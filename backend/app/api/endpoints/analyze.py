from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import traceback, zipfile, shutil, os

from app.schemas import AnalyzeRequest
from app.utils.analysis_manager import LATEST_CONSTRUCTION  # 只保留缓存
from app.utils.Run_test import (
    DifferentialAnalyse,
    ImpossibleAnalyse,
    IntegralAnalyse,
    LinearAnalyse,
    ZeroCorrelationAnalyse,
)
from app.utils.str_util import str2bool, str2list, str2list2

router = APIRouter()


def inject_round_function(analyze_type: str):
    """拷贝模板并把用户提交的轮函数插入到对应分析文件"""

    # 分析类型到模板文件名的映射
    type_map = {
        "dc": "DIF",
        "lc": "Linear",
        "zlc": "ZeroCorrelation",
        "idc": "Impossible",
        "ic": "Integral",  
    }

    file_prefix = type_map.get(analyze_type, analyze_type)
    template_path = f"app/utils/analysis/templates/{file_prefix}.py.bak"
    target_path = f"app/utils/analysis/{file_prefix}.py"

    if not os.path.exists(template_path):
        print(f"❌ 模板文件不存在: {template_path}")
        return

    # 拷贝模板
    shutil.copyfile(template_path, target_path)

    # 读取轮函数
    rf_path = "app/utils/analysis/result/round_function.txt"
    if os.path.exists(rf_path):
        with open(rf_path, "r", encoding="utf-8") as f:
            round_code = f.read()

        if round_code.strip():
            with open(target_path, "a", encoding="utf-8") as f:
                f.write("\n")
                for line in round_code.splitlines():
                    # 默认追加 4 空格缩进（类内函数常用）
                    f.write("    " + line + "\n")
            print(f"✅ 已将轮函数注入到 {target_path}")
    else:
        print("⚠️ 未找到 round_function.txt，跳过注入")

@router.post("/")
async def analyze(request: AnalyzeRequest):
    try:
        # ✅ 如果前端没传构造参数，则自动用第一步保存的结果补充
        if not request.blockLength and "blockLength" in LATEST_CONSTRUCTION:
            print("使用缓存的构造结果")
            request.blockLength = LATEST_CONSTRUCTION.get("blockLength")
            request.branchNumber = LATEST_CONSTRUCTION.get("branchNumber")
            request.bitPermutation = LATEST_CONSTRUCTION.get("bitPermutation")
            request.linearMatrix = LATEST_CONSTRUCTION.get("linearMatrix")
            request.sBoxLength = LATEST_CONSTRUCTION.get("sBoxLength")
            request.sBoxContent = LATEST_CONSTRUCTION.get("sBoxContent")
            request.nonLinearComponent = LATEST_CONSTRUCTION.get("nonLinearComponent")

        # ✅ 参数预处理逻辑
        if str(request.bitPermutation).lower() in ["false", "0", "no"]:
            request.linearMatrix = "0 1\n1 0"

        if request.nonLinearComponent == "modulo":
            request.sBoxLength = 2
            request.sBoxContent = [0, 1, 2, 3]
            request.linearMatrix = "0 1\n1 0"

        # ✅ 公共参数转换
        sbox = []
        if request.sBoxContent:
            if isinstance(request.sBoxContent, str):
                sbox = str2list(request.sBoxContent)
            else:
                sbox = request.sBoxContent
        else:
            sbox = []

        matrix = []
        if request.linearMatrix:
            if isinstance(request.linearMatrix, str):
                matrix = str2list2(request.linearMatrix)
            elif isinstance(request.linearMatrix, list):
                matrix = request.linearMatrix  # 直接用

        non_linear = ""
        if request.nonLinearComponent:
            if isinstance(request.nonLinearComponent, list):
                non_linear = request.nonLinearComponent[0]
            elif isinstance(request.nonLinearComponent, dict):
                non_linear = list(request.nonLinearComponent.values())[0]
            elif isinstance(request.nonLinearComponent, str):
                non_linear = request.nonLinearComponent

        print("=== 收到分析请求 ===")
        print("analyzeType:", request.analyzeType)
        print("blockLength:", request.blockLength,
              "branchNumber:", request.branchNumber,
              "sBoxLength:", request.sBoxLength)
        print("bitPermutation:", request.bitPermutation)
        print("nonLinearComponent", request.nonLinearComponent)

        # ✅ 注入轮函数（模板替换）
        inject_round_function(request.analyzeType)

        result = None
        route_file = None

        # ✅ 各类分析逻辑
        if request.analyzeType == "dc":
            result = DifferentialAnalyse(
                request.blockLength, 5,
                request.branchNumber, request.sBoxLength, sbox, matrix, non_linear
            )
            route_file = "app/utils/analysis/result/差分.txt"

        elif request.analyzeType == "idc":
            result = ImpossibleAnalyse(
                request.blockLength, 6,
                request.branchNumber, request.sBoxLength, sbox, matrix, non_linear
            )

        elif request.analyzeType == "lc":
            result = LinearAnalyse(
                request.blockLength, 5,
                request.branchNumber, request.sBoxLength, sbox, matrix, non_linear
            )
            route_file = "app/utils/analysis/result/线性.txt"

        elif request.analyzeType == "zlc":
            result = ZeroCorrelationAnalyse(
                request.blockLength, 4,
                request.branchNumber, request.sBoxLength, sbox, matrix, non_linear
            )

        else:  # integral
            result = IntegralAnalyse(
                request.blockLength, 6,
                request.branchNumber, request.sBoxLength, sbox, matrix, non_linear
            )
            route_file = "app/utils/analysis/result/积分.txt"

        # ✅ 写 result.txt
        with open("app/utils/analysis/result/result.txt", "w") as f:
            f.write("\n".join([str(e) for e in result]))

        # ✅ 写 route.txt（只有部分分析类型有）
        if route_file:
            with open("app/utils/analysis/result/route.txt", "w") as f:
                f.write(open(route_file, "r").read())
        else:
            open("app/utils/analysis/result/route.txt", "w").close()

        # ✅ 压缩结果
        with zipfile.ZipFile("app/utils/analysis/result/archive.zip", "w") as z:
            z.write("app/utils/analysis/result/result.txt")
            z.write("app/utils/analysis/result/route.txt")

        return JSONResponse(
            {
                "msg": "ok",
                "code": 0,
                "data": {
                    "result": open("app/utils/analysis/result/result.txt", "r").read(),
                    "url_result": "http://127.0.0.1:8000/app/utils/analysis/result/result.txt",
                    "url_route": "http://127.0.0.1:8000/app/utils/analysis/result/route.txt",
                    "url_archive": "http://127.0.0.1:8000/app/utils/analysis/result/archive.zip",
                },
            }
        )

    except Exception as e:
        print("=== 分析报错 ===")
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))
