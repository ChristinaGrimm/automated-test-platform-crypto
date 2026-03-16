import os
import shutil

# 获取当前文件所在目录 (app/utils)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 定位到 templates 目录
TEMPLATE_DIR = os.path.join(BASE_DIR, "analysis", "templates")

# 分析文件输出目录 (app/utils/analysis)
ANALYSIS_DIR = os.path.join(BASE_DIR, "analysis")

# ✅ 用于保存最新构造结果（仅内存，不落库）
LATEST_CONSTRUCTION: dict = {}

ANALYZE_TYPE_MAP = {
    "dc": "DIF",
    "lc": "Linear",
    "ic": "Integral",
    "idc": "Impossible",
    "zlc": "ZeroCorrelation",
}

def prepare_analysis_file(analyze_type: str, code: str):
    template_base = ANALYZE_TYPE_MAP.get(analyze_type)
    if not template_base:
        raise ValueError(f"Unsupported analyzeType: {analyze_type}")

    template_file = f"{template_base}.py.bak"
    src = os.path.join(TEMPLATE_DIR, template_file)
    dst = os.path.join(ANALYSIS_DIR, f"{template_base}.py")

    if not os.path.exists(src):
        raise FileNotFoundError(f"Template not found: {src}")

    with open(src, "r", encoding="utf-8") as f:
        template_content = f.read()

    with open(dst, "w", encoding="utf-8") as f:
        f.write(template_content)

        # 在类里追加轮函数代码（缩进 4 个空格）
        if code and code.strip():
            f.write("\n")
            for line in code.split("\n"):
                f.write("    " + line + "\n")

    print(f"生成分析文件: {dst}")
    return dst
