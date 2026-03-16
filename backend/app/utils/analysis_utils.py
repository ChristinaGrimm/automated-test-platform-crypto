# backend/app/utils/analysis_utils.py
import importlib
from typing import Any, Dict, Optional

from app.utils.analysis_manager import prepare_analysis_file, ANALYZE_TYPE_MAP

# 映射 analyzeType -> 分析类名（在模块中）
CLASS_NAME_MAP = {
    "dc": "Difference",
    "lc": "Linear",
    "ic": "Integral",
    "idc": "Impossible",
    "zlc": "ZeroCorrelation",
}

def _get_param(params: Dict[str, Any], keys, default=None):
    """尝试从多个可能的键中取值（keys 可为 str 或 iterable），返回第一个非 None 值。"""
    if isinstance(keys, str):
        keys = [keys]
    for k in keys:
        # 支持点分层（如 "blockMatrixForm.blockLength"）和普通键
        if isinstance(k, str) and "." in k:
            top, rest = k.split(".", 1)
            if top in params and isinstance(params[top], dict):
                v = params[top].get(rest)
                if v is not None:
                    return v
        else:
            v = params.get(k)
            if v is not None:
                return v
    return default

def perform_analysis(request_or_dict) -> Dict[str, Any]:
    """
    执行分析：
    - 接收 Pydantic 模型对象 或 dict
    - prepare_analysis_file 生成 .py
    - 动态导入模块并 reload（以加载最新拼接代码）
    - 实例化对应分析类并调用 genEncryptSubjection(round)
    返回结构化结果（constraints 列表，vars 列表若存在）
    """
    # 支持传入 Pydantic 对象或 dict
    if hasattr(request_or_dict, "dict"):
        params = request_or_dict.dict()
    else:
        params = dict(request_or_dict or {})

    analyze_type = _get_param(params, ["analyzeType", "analyze_type"], default=None)
    if analyze_type is None:
        raise ValueError("Missing analyzeType in request")

    analyze_type = analyze_type.lower()

    code = _get_param(params, ["code"], default="")
    # round 可缺省；默认 1
    round_num = _get_param(params, ["round", "rounds"], default=1)
    try:
        round_num = int(round_num)
    except Exception:
        round_num = 1

    # 先生成/拼接目标 .py 文件（会覆盖 utils/analysis/<Name>.py）
    prepare_analysis_file(analyze_type, code)

    # 动态导入对应模块并 reload
    if analyze_type not in ANALYZE_TYPE_MAP:
        raise ValueError(f"Unsupported analyzeType: {analyze_type}")
    module_name = f"app.utils.analysis.{ANALYZE_TYPE_MAP[analyze_type]}"
    try:
        module = importlib.import_module(module_name)
        importlib.reload(module)
    except Exception as e:
        raise ImportError(f"Failed importing analysis module {module_name}: {e}")

    # 拿到类并实例化（从多个可能来源读取构造参数）
    class_name = CLASS_NAME_MAP.get(analyze_type)
    if not class_name:
        raise ValueError(f"No class mapping for analyzeType {analyze_type}")

    try:
        AnalyzerClass = getattr(module, class_name)
    except AttributeError:
        raise AttributeError(f"Class {class_name} not found in module {module_name}")

    # 从请求中获取构造参数（容错多个可能键名）
    blockLength = _get_param(params, ["blockLength", "block_size"], default=None)
    branchNumber = _get_param(params, ["branchNumber", "branch_number"], default=None)
    linearMatrix = _get_param(params, ["linearMatrix", "blockMatrix", "blockMatrixForm", "matrix"], default=None)
    bitPermutation = _get_param(params, ["bitPermutation", "permutation"], default=None)
    sBoxLength = _get_param(params, ["sBoxLength", "sbox_length"], default=None)
    sBoxContent = _get_param(params, ["sBoxContent", "sbox", "SboxContent"], default=None)
    nonLinearComponent = _get_param(params, ["nonLinearComponent", "nonlinear"], default=None)

    # 某些关键参数缺失时只给出提示（不强制失败，以便用户按需）
    # 这里你可以根据分析类要求决定是否强制报错
    # 如果 blockLength/branchNumber 等是必须的，可以在此抛错
    if blockLength is None:
        # 不是必需就用默认 0 或抛错
        # raise ValueError("blockLength is required for analysis")
        blockLength = 0

    # 实例化
    analyzer = AnalyzerClass(
        blockLength,
        round_num,
        branchNumber,
        sBoxLength,
        sBoxContent,
        linearMatrix,
        nonLinearComponent,
    )

    # 调用分析入口（约定：genEncryptSubjection）
    if not hasattr(analyzer, "genEncryptSubjection"):
        raise AttributeError(f"Analyzer class {class_name} has no method genEncryptSubjection")

    constraints = analyzer.genEncryptSubjection(round_num)
    vars_decl = None
    if hasattr(analyzer, "getVars"):
        try:
            vars_decl = analyzer.getVars(round_num)
        except Exception:
            vars_decl = None

    return {"constraints": constraints, "vars": vars_decl}
