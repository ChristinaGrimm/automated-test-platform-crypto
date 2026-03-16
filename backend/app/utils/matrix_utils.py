import concurrent.futures
import itertools
import os
import random
import re
import subprocess
import threading
import time
import numpy as np
import uuid
from typing import List, Dict, Any, Optional
from app.schemas import BitMatrixRequest

# 确保临时目录存在
if not os.path.exists("temp"):
    os.makedirs("temp")

def generate_np_vectors(n):
    vectors = []
    for i in range(n):
        vector = np.zeros(n)
        vector[i] = 1
        vectors.append(vector)
    return vectors

def find(n, xor, path):
    x = generate_np_vectors(n)
    for i in range(xor):
        pattern = rf"ASSERT\( a{i}_[a-zA-Z0-9_]+ = 0b1 \);"
        with open(f"temp/{path}", "r") as file:
            file_contents = file.read()
            matches = re.findall(pattern, file_contents)
        vec = np.zeros(n)
        for j in range(len(matches)):
            pattern = rf"a{i}_(\d+) = 0b1 "
            match2 = re.search(pattern, matches[j])
            if match2:
                number_between = int(match2.group(1))
                vec = (vec + x[number_between]) % 2
        x.append(vec)
    result_matrix = np.array(x[xor:], dtype=int)
    return result_matrix

def hamming_weight_vectors(n, i):
    all_vectors = itertools.product("01", repeat=n)
    hamming_i_vectors = set()
    for vector in all_vectors:
        if vector.count("1") == i:
            hamming_i_vectors.add("".join(vector))
    vectors = list(hamming_i_vectors)
    random.shuffle(vectors)
    return vectors

def hamming_weight(s):
    return s.count("1")

def input_vector(n, file):
    for i in range(n):
        file.write(f"x{i}")
        if i != n - 1:
            file.write(",")
        else:
            file.write(f":BITVECTOR({n});\n")
    vec_str = "0" * n
    vec_str = "1" + vec_str[1:]
    for i in range(n):
        file.write(f"ASSERT(x{i}=0bin{vec_str});\n")
        index = vec_str.find("1")
        if index != -1 and index < len(vec_str) - 1:
            vec_str = vec_str[:index] + "0" + "1" + vec_str[index + 2:]
    file.write("\n\n")

def alldepth(n, xor, file):
    for i in range(n + xor):
        file.write(f"depth{i}")
        if i != n + xor - 1:
            file.write(",")
        else:
            file.write(":BITVECTOR(4);\n\n")
    for i in range(n):
        file.write(f"ASSERT(depth{i}=0b0001);\n")

def eachxor(n, i, file):
    for j in range(n + i):
        file.write(f"a{i}_{j}")
        if j != n + i - 1:
            file.write(",")
        else:
            file.write(f",c{i}:BITVECTOR(1);\n")
    
    file.write(f"ASSERT(BVPLUS(9,")
    for j in range(n + i):
        file.write(f"0bin00000000@a{i}_{j}")
        if j != n + i - 1:
            file.write(",")
        else:
            file.write(f")=0bin000000010);\n")
    
    file.write(f"ASSERT(x{n + i}=")
    for j in range(n + i - 1):
        file.write(f"BVXOR(")
    for j in range(n + i):
        file.write(f"BVMULT({n},0bin{'0' * (n - 1)}@a{i}_{j},x{j})")
        if j == 0:
            file.write(f",")
        if j != 0 and j != n + i - 1:
            file.write(f"),")
        if j == n + i - 1:
            file.write(f"));\n\n")
    
    for j in range(n + i):
        count = 0
        file.write(f"ASSERT(")
        for k in range(n + i):
            if k != j:
                file.write(f"BVGE(BVMULT(4,0b000@a{i}_{j},depth{j}),BVMULT(4,0b000@a{i}_{k},depth{k}))")
                count = count + 1
                if count < n + i - 1:
                    file.write(f" AND ")
                else:
                    file.write(f" => depth{n + i}=BVPLUS(4,depth{j},0b0001));\n")
    file.write("\n")
    
    for j in range(n + i):
        file.write(f"ASSERT(IF a{i}_{j}=0bin1 THEN (BVGE(BVPLUS(5")
        for k in range(n):
            file.write(f",0bin0000@x{n + i}[{k}:{k}]")
        file.write(f"),BVPLUS(5")
        for k in range(n):
            file.write(f",0bin0000@x{j}[{k}:{k}]")
        file.write(f"))) ELSE c{i}=0b0 ENDIF);\n")
    file.write("\n")

def ifinvertible(n, xor, file):
    for i in range(n):
        if i != n - 1:
            file.write(f"inv{i},identy{i},")
        if i == n - 1:
            file.write(f"inv{i},identy{i}:BITVECTOR({n});\n\n")
    for i in range(n):
        file.write(f"ASSERT(identy{i}=")
        for j in range(n):
            if j != n - 1:
                for k in range(n - 1):
                    file.write(f"BVXOR(")
                for l in range(n):
                    if l == 0:
                        file.write(f"BVMULT(1,x{n + xor - 1 - j}[{l}:{l}],inv{i}[{l}:{l}]),")
                    if l != 0 and l != n - 1:
                        file.write(f"BVMULT(1,x{n + xor - 1 - j}[{l}:{l}],inv{i}[{l}:{l}])),")
                    if l == n - 1:
                        file.write(f"BVMULT(1,x{n + xor - 1 - j}[{l}:{l}],inv{i}[{l}:{l}]))@")
            if j == n - 1:
                for k in range(n - 1):
                    file.write(f"BVXOR(")
                for l in range(n):
                    if l == 0:
                        file.write(f"BVMULT(1,x{n + xor - 1 - j}[{l}:{l}],inv{i}[{l}:{l}]),")
                    if l != 0 and l != n - 1:
                        file.write(f"BVMULT(1,x{n + xor - 1 - j}[{l}:{l}],inv{i}[{l}:{l}])),")
                    if l == n - 1:
                        file.write(f"BVMULT(1,x{n + xor - 1 - j}[{l}:{l}],inv{i}[{l}:{l}])));\n\n\n")
    
    vec_str2 = "0" * n
    vec_str2 = "1" + vec_str2[1:]
    for i in range(n):
        file.write(f"ASSERT(identy{i}=0bin{vec_str2});\n")
        index2 = vec_str2.find("1")
        if index2 != -1 and index2 < len(vec_str2) - 1:
            vec_str2 = vec_str2[:index2] + "0" + "1" + vec_str2[index2 + 2:]
    file.write("\n\n")

def branchnumber(n, bd, xor, file):
    if (bd - 1) % 2 != 0:
        for i in range(int(bd / 2)):  # 对于1到分指数一半+1的汉明重量的向量
            hm = i + 1
            vectors = hamming_weight_vectors(n, hm)  # 生成汉明重量为hm的n维向量

            for j in range(len(vectors)):  # 对于每个向量

                midhm = hamming_weight(vectors[j])  # 储存当前的汉明重量
                file.write(f"ASSERT(BVGE(BVPLUS(6,")
                for k in range(n):
                    file.write(f"0b00000@")
                    weight = midhm

                    for e in range(hm - 1):
                        file.write(f"BVXOR(")
                    for g in range(n):
                        if vectors[j][g] == "1":
                            file.write(f"x{n+xor-1-k}[{g}:{g}]")
                            if hm == 1 and k != n - 1:
                                file.write(f",")
                            if hm == 1 and k == n - 1:
                                file.write(f"),")
                            if hm != 1 and k != n - 1 and weight == midhm:
                                file.write(f",")
                            if hm != 1 and k != n - 1 and weight != midhm:
                                file.write(f"),")
                            if hm != 1 and k == n - 1 and weight == midhm:
                                file.write(f",")
                            if (
                                hm != 1
                                and k == n - 1
                                and weight != midhm
                                and weight != 1
                            ):
                                file.write(f"),")
                            if hm != 1 and k == n - 1 and weight == 1:
                                file.write(f")),")
                            weight = weight - 1
                file.write(f"0b{bin(bd-midhm)[2:].zfill(6)}));\n\n")

        for i in range(int(bd / 2 - 1)):
            hm = i + 1
            vectors = hamming_weight_vectors(n, hm)
            for j in range(len(vectors)):
                midhm2 = hamming_weight(vectors[j])
                file.write(f"ASSERT(BVGE(BVPLUS(6,")
                for k in range(n):
                    file.write(f"0b00000@")
                    weight2 = midhm2
                    for e in range(hm - 1):
                        file.write(f"BVXOR(")
                    for g in range(n):

                        if vectors[j][g] == "1":

                            file.write(f"inv{g}[{k}:{k}]")
                            if hm == 1 and k != n - 1:
                                file.write(f",")
                            if hm == 1 and k == n - 1:
                                file.write(f"),")
                            if hm != 1 and k != n - 1 and weight2 == midhm2:
                                file.write(f",")
                            if hm != 1 and k != n - 1 and weight2 != midhm2:
                                file.write(f"),")
                            if hm != 1 and k == n - 1 and weight2 == midhm2:
                                file.write(f",")
                            if (
                                hm != 1
                                and k == n - 1
                                and weight2 != 1
                                and weight2 != midhm2
                            ):
                                file.write(f"),")
                            if hm != 1 and k == n - 1 and weight2 == 1:
                                file.write(f")),")
                            weight2 = weight2 - 1
                file.write(f"0b{bin(bd-midhm2)[2:].zfill(6)}));\n\n")

    if (bd - 1) % 2 == 0:
        for i in range(int(bd / 2)):
            hm = i + 1
            vectors = hamming_weight_vectors(n, hm)
            for j in range(len(vectors)):

                midhm3 = hamming_weight(vectors[j])
                file.write(f"ASSERT(BVGE(BVPLUS(6,")
                for k in range(n):
                    file.write(f"0b00000@")
                    weight3 = midhm3

                    for e in range(hm - 1):
                        file.write(f"BVXOR(")
                    for g in range(n):
                        if vectors[j][g] == "1":
                            file.write(f"x{n + xor - 1 - k}[{g}:{g}]")
                            if hm == 1 and k != n - 1:
                                file.write(f",")
                            if hm == 1 and k == n - 1:
                                file.write(f"),")
                            if hm != 1 and k != n - 1 and weight3 == midhm3:
                                file.write(f",")
                            if hm != 1 and k != n - 1 and weight3 != midhm3:
                                file.write(f"),")
                            if hm != 1 and k == n - 1 and weight3 == midhm3:
                                file.write(f",")
                            if (
                                hm != 1
                                and k == n - 1
                                and weight3 != midhm3
                                and weight3 != 1
                            ):
                                file.write(f"),")
                            if hm != 1 and k == n - 1 and weight3 == 1:
                                file.write(f")),")
                            weight3 = weight3 - 1
                file.write(f"0b{bin(bd - midhm3)[2:].zfill(6)}));\n\n")

                file.write(f"ASSERT(BVGE(BVPLUS(6,")
                for k in range(n):
                    file.write(f"0b00000@")
                    weight4 = midhm3
                    for e in range(hm - 1):
                        file.write(f"BVXOR(")
                    for g in range(n):

                        if vectors[j][g] == "1":

                            file.write(f"inv{g}[{k}:{k}]")
                            if hm == 1 and k != n - 1:
                                file.write(f",")
                            if hm == 1 and k == n - 1:
                                file.write(f"),")
                            if hm != 1 and k != n - 1 and weight4 == midhm3:
                                file.write(f",")
                            if hm != 1 and k != n - 1 and weight4 != midhm3:
                                file.write(f"),")
                            if hm != 1 and k == n - 1 and weight4 == midhm3:
                                file.write(f",")
                            if (
                                hm != 1
                                and k == n - 1
                                and weight4 != 1
                                and weight4 != midhm3
                            ):
                                file.write(f"),")
                            if hm != 1 and k == n - 1 and weight4 == 1:
                                file.write(f")),")
                            weight4 = weight4 - 1
                file.write(f"0b{bin(bd - midhm3)[2:].zfill(6)}));\n\n")
    # 差分分指数

    file.write(f"\n\n")
    # 线性分指数
    if (bd - 1) % 2 != 0:
        for i in range(int(bd / 2)):  # 对于1到分指数一半+1的汉明重量的向量
            hm = i + 1
            vectors = hamming_weight_vectors(n, hm)  # 生成汉明重量为hm的n维向量

            for j in range(len(vectors)):  # 对于每个向量

                midhm = hamming_weight(vectors[j])  # 储存当前的汉明重量
                file.write(f"ASSERT(BVGE(BVPLUS(6,")
                for k in range(n):
                    file.write(f"0b00000@")
                    weight = midhm

                    for e in range(hm - 1):
                        file.write(f"BVXOR(")
                    for g in range(n):
                        if vectors[j][g] == "1":
                            file.write(f"inv{k}[{g}:{g}]")
                            if hm == 1 and k != n - 1:
                                file.write(f",")
                            if hm == 1 and k == n - 1:
                                file.write(f"),")
                            if hm != 1 and k != n - 1 and weight == midhm:
                                file.write(f",")
                            if hm != 1 and k != n - 1 and weight != midhm:
                                file.write(f"),")
                            if hm != 1 and k == n - 1 and weight == midhm:
                                file.write(f",")
                            if (
                                hm != 1
                                and k == n - 1
                                and weight != midhm
                                and weight != 1
                            ):
                                file.write(f"),")
                            if hm != 1 and k == n - 1 and weight == 1:
                                file.write(f")),")
                            weight = weight - 1
                file.write(f"0b{bin(bd - midhm)[2:].zfill(6)}));\n\n")

        for i in range(int(bd / 2 - 1)):
            hm = i + 1
            vectors = hamming_weight_vectors(n, hm)
            for j in range(len(vectors)):
                midhm2 = hamming_weight(vectors[j])
                file.write(f"ASSERT(BVGE(BVPLUS(6,")
                for k in range(n):
                    file.write(f"0b00000@")
                    weight2 = midhm2
                    for e in range(hm - 1):
                        file.write(f"BVXOR(")
                    for g in range(n):

                        if vectors[j][g] == "1":

                            file.write(f"x{n+xor-1-g}[{k}:{k}]")
                            if hm == 1 and k != n - 1:
                                file.write(f",")
                            if hm == 1 and k == n - 1:
                                file.write(f"),")
                            if hm != 1 and k != n - 1 and weight2 == midhm2:
                                file.write(f",")
                            if hm != 1 and k != n - 1 and weight2 != midhm2:
                                file.write(f"),")
                            if hm != 1 and k == n - 1 and weight2 == midhm2:
                                file.write(f",")
                            if (
                                hm != 1
                                and k == n - 1
                                and weight2 != 1
                                and weight2 != midhm2
                            ):
                                file.write(f"),")
                            if hm != 1 and k == n - 1 and weight2 == 1:
                                file.write(f")),")
                            weight2 = weight2 - 1
                file.write(f"0b{bin(bd - midhm2)[2:].zfill(6)}));\n\n")

    if (bd - 1) % 2 == 0:
        for i in range(int(bd / 2)):
            hm = i + 1
            vectors = hamming_weight_vectors(n, hm)
            for j in range(len(vectors)):

                midhm3 = hamming_weight(vectors[j])
                file.write(f"ASSERT(BVGE(BVPLUS(6,")
                for k in range(n):
                    file.write(f"0b00000@")
                    weight3 = midhm3

                    for e in range(hm - 1):
                        file.write(f"BVXOR(")
                    for g in range(n):
                        if vectors[j][g] == "1":
                            file.write(f"inv{k}[{g}:{g}]")
                            if hm == 1 and k != n - 1:
                                file.write(f",")
                            if hm == 1 and k == n - 1:
                                file.write(f"),")
                            if hm != 1 and k != n - 1 and weight3 == midhm3:
                                file.write(f",")
                            if hm != 1 and k != n - 1 and weight3 != midhm3:
                                file.write(f"),")
                            if hm != 1 and k == n - 1 and weight3 == midhm3:
                                file.write(f",")
                            if (
                                hm != 1
                                and k == n - 1
                                and weight3 != midhm3
                                and weight3 != 1
                            ):
                                file.write(f"),")
                            if hm != 1 and k == n - 1 and weight3 == 1:
                                file.write(f")),")
                            weight3 = weight3 - 1
                file.write(f"0b{bin(bd - midhm3)[2:].zfill(6)}));\n\n")

                file.write(f"ASSERT(BVGE(BVPLUS(6,")
                for k in range(n):
                    file.write(f"0b00000@")
                    weight4 = midhm3
                    for e in range(hm - 1):
                        file.write(f"BVXOR(")
                    for g in range(n):

                        if vectors[j][g] == "1":

                            file.write(f"x{n+xor-1-g}[{k}:{k}]")
                            if hm == 1 and k != n - 1:
                                file.write(f",")
                            if hm == 1 and k == n - 1:
                                file.write(f"),")
                            if hm != 1 and k != n - 1 and weight4 == midhm3:
                                file.write(f",")
                            if hm != 1 and k != n - 1 and weight4 != midhm3:
                                file.write(f"),")
                            if hm != 1 and k == n - 1 and weight4 == midhm3:
                                file.write(f",")
                            if (
                                hm != 1
                                and k == n - 1
                                and weight4 != 1
                                and weight4 != midhm3
                            ):
                                file.write(f"),")
                            if hm != 1 and k == n - 1 and weight4 == 1:
                                file.write(f")),")
                            weight4 = weight4 - 1
                file.write(f"0b{bin(bd - midhm3)[2:].zfill(6)}));\n\n")


def main(n, xor, bd, depth, path):
    depth = depth + 1
    with open(f"temp/{path}.cvc", "w") as file:
        input_vector(n, file)
        for i in range(xor):
            file.write(f"x{n+i}")
            if i != xor - 1:
                file.write(",")
            if i == xor - 1:
                file.write(f":BITVECTOR({n});\n")
        file.write("\n\n")
        
        alldepth(n, xor, file)
        
        for i in range(xor):
            eachxor(n, i, file)
        
        for i in range(xor):
            file.write(f"ASSERT(BVLE(depth{i+n},0bin{bin(depth)[2:].zfill(4)}));\n")
        
        for b in range(n):
            file.write(f"ASSERT(BVGE(BVPLUS(5")
            for k in range(n):
                file.write(f",0bin0000@x{n+xor-1-b}[{k}:{k}]")
            file.write(f"),0bin{bin(bd-1)[2:].zfill(5)}));\n")
        
        for l in range(n):
            for o in range(xor + l + 1, n + xor):
                file.write(f"ASSERT(x{xor+l}/=x{o});\n")
        file.write("\n\n")
        
        for c in range(n):
            file.write(f"ASSERT(BVGE(BVPLUS(5")
            for b in range(n):
                file.write(f",0bin0000@x{n+xor-1-b}[{c}:{c}]")
            file.write(f"),0bin{bin(bd-1)[2:].zfill(5)}));\n")
        file.write("\n\n")
        
        for l1 in range(n):
            for o1 in range(l1 + 1, n):
                file.write(f"ASSERT(")
                for z in range(n):
                    if z != n - 1:
                        file.write(f"x{n+xor-1-z}[{l1}:{l1}]@")
                    if z == n - 1:
                        file.write(f"x{n+xor-1-z}[{l1}:{l1}]/=")
                for z2 in range(n):
                    if z2 != n - 1:
                        file.write(f"x{n+xor-1-z2}[{o1}:{o1}]@")
                    if z2 == n - 1:
                        file.write(f"x{n+xor-1-z2}[{o1}:{o1}]);\n")
        file.write("\n\n")
        
        ifinvertible(n, xor, file)
        branchnumber(n, bd, xor, file)
        file.write("QUERY(FALSE);\nCOUNTEREXAMPLE;")

def solve(n, xor, bd, depth):
    rand_str = uuid.uuid4().hex[:6]
    path = f"{n}_{xor}_{bd}_{depth}_{rand_str}"
    main(n, xor, bd, depth, path)
    
    try:
        subprocess.run(
            f"stp temp/{path}.cvc > temp/{path}.txt",
            shell=True,
            check=True,
            timeout=300  # 设置超时时间为5分钟
        )
        with open(f"temp/{path}.txt", "r") as file:
            file_contents = file.read()
            if "Valid." in file_contents:
                return None
            else:
                res = find(n, xor, f"{path}.txt")
                return res.tolist()
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
        return None
    finally:
        # 清理临时文件
        try:
            os.remove(f"temp/{path}.cvc")
            os.remove(f"temp/{path}.txt")
        except:
            pass

def construct_bit_matrix(params: BitMatrixRequest) -> List[List[List[int]]]:
    """
    构造比特矩阵的主函数
    """
    n = params.block_size
    xor = params.xor_count
    bd = params.branch_number
    depth = params.depth
    quantity = params.quantity
    
    results = []
    
    if n >= 8 and quantity > 1:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(solve, n, xor, bd, depth) for _ in range(quantity)]
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result is not None:
                    results.append(result)
    else:
        for _ in range(quantity):
            result = solve(n, xor, bd, depth)
            if result is not None:
                results.append(result)
    
    return results



