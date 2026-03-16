import random
import re
import subprocess
import os
import logging
import tempfile
from typing import List, Dict, Any
from pathlib import Path

# 配置日志
logger = logging.getLogger(__name__)

current_dir = Path(__file__).parent

# 确保临时目录存在 (backend/temp)
temp_dir = (current_dir.parent.parent / "temp").resolve()
temp_dir.mkdir(exist_ok=True)

def find_sbox_values(n: int, file_path: str) -> List[int]:
    """
    从STP求解器输出文件中提取S盒值
    
    参数:
        n: S盒大小 (2^bit_num)
        file_path: 输出文件路径
        
    返回:
        S盒值列表
    """
    extracted_values = []
    for i in range(n):
        if i < 10:
            value = str(i)
        else:
            value = chr(ord("A") + (i - 10))
        pattern = rf"ASSERT\( S\[0x{value}\] = 0x([0-9a-fA-F]+) \);"

        try:
            with open(file_path, "r") as file:
                file_contents = file.read()
                matches = re.findall(pattern, file_contents)
                if matches:
                    for match in matches:
                        extracted_values.append(int(match, 16))
                else:
                    logger.warning(f"在文件 {file_path} 中未找到匹配的S盒值")
        except Exception as e:
            logger.error(f"读取S盒值文件时出错: {str(e)}")
            raise
    
    return extracted_values

def start_sbox_process(
    bit_num: int, 
    diff_uniform: int, 
    linear_uniform: int, 
    dbn: int, 
    lbn: int, 
    bibo_ddt: int, 
    bibo_lat: int, 
    out_path: str
) -> subprocess.Popen:
    """
    启动S盒构造进程
    
    参数:
        bit_num: S盒位数
        diff_uniform: 差分均匀度
        linear_uniform: 线性均匀度
        dbn: 差分分支数
        lbn: 线性分支数
        bibo_ddt: BIBO DDT
        bibo_lat: BIBO LAT
        out_path: 输出文件路径
        
    返回:
        subprocess.Popen对象
    """
    # 确保核心工具存在
    core_tool_path = current_dir / "sbox_construction"
    if not core_tool_path.exists():
        raise FileNotFoundError(f"S盒构造工具未找到: {core_tool_path}")
    
    if not os.access(core_tool_path, os.X_OK):
        raise PermissionError(f"S盒构造工具没有执行权限: {core_tool_path}")
    
    try:
        process = subprocess.Popen(
            [
                str(core_tool_path),
                f"{dbn}",
                f"{lbn}",
                f"{diff_uniform}",
                f"{linear_uniform}",
                f"{bibo_ddt}",
                f"{bibo_lat}",
                f"{bit_num}",
                out_path,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return process
    except Exception as e:
        logger.error(f"启动S盒构造进程失败: {str(e)}")
        raise

def solve_sbox(
    bit_num: int, 
    diff_uniform: int, 
    linear_uniform: int, 
    dbn: int, 
    lbn: int, 
    bibo_ddt: int, 
    bibo_lat: int, 
    quantity: int
) -> List[List[int]]:
    """
    构造S盒的主函数
    
    参数:
        bit_num: S盒位数
        diff_uniform: 差分均匀度
        linear_uniform: 线性均匀度
        dbn: 差分分支数
        lbn: 线性分支数
        bibo_ddt: BIBO DDT
        bibo_lat: BIBO LAT
        quantity: 生成数量
        
    返回:
        S盒列表，每个S盒是一个整数值列表
    """
    results = []
    
    # 生成随机文件名
    # rand_str = ''.join(random.sample("abcdefghijklmnopqrstuvwxyz0123456789", 6))
    # cvc_path = temp_dir / f"sbox_{rand_str}"
    # result_path = f"{cvc_path}.txt"
    rand_str = ''.join(random.sample("abcdefghijklmnopqrstuvwxyz0123456789", 6))
    cvc_path = temp_dir / f"sbox_{rand_str}"
    result_path = temp_dir / f"sbox_{rand_str}.txt"

    
    logger.info(f"开始构造S盒: bit_num={bit_num}, diff_uniform={diff_uniform}, quantity={quantity}")
    
    try:
        # 第一步构造
        process = start_sbox_process(
            bit_num, diff_uniform, linear_uniform, dbn, lbn, bibo_ddt, bibo_lat, f"{cvc_path}.cvc"
        )
        process.wait()
        
        if process.returncode != 0:
            stderr = process.stderr.read().decode() if process.stderr else "未知错误"
            logger.error(f"S盒构造进程失败: {stderr}")
            return results
        
        logger.info("S盒CVC文件构造完成")

        # 调用 STP 之前确认文件存在
        if not os.path.exists(f"{cvc_path}.cvc"):
            logger.error(f"CVC 文件未生成: {cvc_path}.cvc")
            return results
        
        # 运行STP求解器
        # stp_result = subprocess.run(
        #     f"stp {cvc_path}.cvc > {result_path}",
        #     shell=True,
        #     capture_output=True,
        #     text=True,
        #     timeout=300  # 5分钟超时
        # )
        stp_result = subprocess.run(
            ["stp", str(cvc_path) + ".cvc"],
            stdout=open(result_path, "w"),
            stderr=subprocess.PIPE,
            text=True,
            timeout=300
        )
        
        if stp_result.returncode != 0:
            logger.error(f"STP求解失败: {stp_result.stderr}")
            return results
        
        # 提取结果
        sbox_values = find_sbox_values(1 << bit_num, result_path)
        if sbox_values:
            results.append(sbox_values)
            logger.info(f"成功构造第1个S盒")
        else:
            logger.warning("第一个S盒构造失败")
            return results
        
        # 构造更多S盒
        if quantity > 1:
            for i in range(2, quantity + 1):
                # 读取结果文件
                with open(result_path, "r") as file:
                    lines = file.readlines()
                
                # 读取原始CVC文件
                with open(f"{cvc_path}.cvc", "r") as file:
                    or_cvc = file.readlines()
                
                # 查找可以反转的约束
                pattern = re.compile(
                    r"ASSERT\( (Counter_(LAT|DDT)\[0x[0-9A-Fa-f]+\] = 0b0) \);"
                )
                matching_lines = [idx for idx, line in enumerate(lines) if pattern.search(line)]
                
                if not matching_lines:
                    logger.warning(f"没有找到可反转的约束，无法生成第{i}个S盒")
                    break
                
                # 随机选择一行进行反转
                selected_index = random.choice(matching_lines)
                lines[selected_index] = lines[selected_index].replace("0b0", "0b1")
                
                # 更新CVC文件
                or_cvc[-3] = f"{lines[selected_index]}\n"
                
                # 保存新的CVC文件
                new_cvc = f"{cvc_path}_{i}.cvc"
                with open(new_cvc, "w") as file:
                    file.writelines(or_cvc)

                # 调用 STP 之前确认文件存在
                if not os.path.exists(f"{cvc_path}.cvc"):
                    logger.error(f"CVC 文件未生成: {cvc_path}.cvc")
                    return results
                
                # 运行STP求解器
                # stp_result = subprocess.run(
                #     f"stp {new_cvc} > {result_path}",
                #     shell=True,
                #     capture_output=True,
                #     text=True,
                #     timeout=300
                # )
                stp_result = subprocess.run(
                    ["stp", new_cvc],
                    stdout=open(result_path, "w"),
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=300
                )
                
                if stp_result.returncode != 0:
                    logger.error(f"STP求解失败: {stp_result.stderr}")
                    continue
                
                # 检查结果是否有效
                with open(result_path, "r") as file:
                    result_content = file.read()
                
                if "Valid." in result_content:
                    logger.warning(f"第{i}个S盒构造失败 (验证有效)")
                    continue
                
                # 提取结果
                sbox_values = find_sbox_values(1 << bit_num, result_path)
                if sbox_values:
                    results.append(sbox_values)
                    logger.info(f"成功构造第{i}个S盒")
                
                # 清理临时文件
                try:
                    os.remove(new_cvc)
                except:
                    pass
    
    except subprocess.TimeoutExpired:
        logger.error("S盒构造超时")
    except Exception as e:
        logger.error(f"S盒构造过程中发生错误: {str(e)}")
    finally:
        # 清理临时文件
        try:
            os.remove(f"{cvc_path}.cvc")
            os.remove(result_path)
        except:
            pass
    
    logger.info(f"S盒构造完成，共生成 {len(results)} 个S盒")
    return results

def construct_sbox(params: Dict[str, Any]) -> List[List[int]]:
    """
    S盒构造API的主函数
    
    参数:
        params: 包含构造参数的字典，应包括:
            input_size: 输入大小(比特)
            output_size: 输出大小(比特)
            diff_uniform: 差分均匀度
            linear_uniform: 线性均匀度
            dbn: 差分分支数
            lbn: 线性分支数
            bibo_ddt: BIBO DDT
            bibo_lat: BIBO LAT
            quantity: 生成数量
    
    返回:
        S盒列表，每个S盒是一个整数值列表
    """
    try:
        logger.info(f"接收到S盒构造参数: {params}")
        
        # 提取参数
        input_size = params.get("input_size", 4)
        output_size = params.get("output_size", 4)
        diff_uniform = params.get("diff_uniform", 4)
        linear_uniform = params.get("linear_uniform", 4)
        dbn = params.get("dbn", 3)
        lbn = params.get("lbn", 3)
        bibo_ddt = params.get("bibo_ddt", 16)
        bibo_lat = params.get("bibo_lat", 16)
        quantity = params.get("quantity", 1)
        
        # 验证参数
        if input_size != output_size:
            logger.warning("输入大小和输出大小不同，这可能不是标准的S盒")
        
        if input_size not in [4, 6, 8]:
            logger.warning(f"不常见的S盒输入大小: {input_size}")
        
        # 调用S盒构造函数
        results = solve_sbox(
            bit_num=input_size,
            diff_uniform=diff_uniform,
            linear_uniform=linear_uniform,
            dbn=dbn,
            lbn=lbn,
            bibo_ddt=bibo_ddt,
            bibo_lat=bibo_lat,
            quantity=quantity
        )
        
        return results
        
    except Exception as e:
        logger.error(f"S盒构造过程中发生错误: {str(e)}")
        raise