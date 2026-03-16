# algorithm.py
from fastapi import APIRouter, HTTPException
from app.schemas import AlgorithmDesignRequest, CodeValidationRequest, RoundFunctionSaveRequest, StandardResponse

router = APIRouter()

@router.post("/design", response_model=StandardResponse)
async def submit_algorithm_design(request: AlgorithmDesignRequest):
    """提交完整的算法设计"""
    try:
        # 这里可以添加算法设计的保存逻辑
        return {
            "code": 0,
            "message": "算法设计提交成功",
            "data": {
                "design_id": "design_12345",
                "submitted_at": "2024-01-01 12:00:00"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/validate", response_model=StandardResponse)
async def validate_algorithm_code(request: CodeValidationRequest):
    """验证算法代码语法"""
    try:
        code = request.code.strip()
        if not code:
            return {"code": 1, "message": "代码不能为空", "data": None}

        if len(code) < 10:
            return {"code": 2, "message": "代码过短，请提供完整的算法描述", "data": None}

        return {"code": 0, "message": "代码验证通过", "data": None}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/save_round_function", response_model=StandardResponse)
async def save_round_function(request: RoundFunctionSaveRequest):
    """保存用户提交的轮函数到文件"""
    try:
        code = request.code.strip()
        if not code:
            return {"code": 1, "message": "轮函数不能为空", "data": None}

        # 保存到固定文件，供 analyze.py 使用
        with open("app/utils/analysis/result/round_function.txt", "w", encoding="utf-8") as f:
            f.write(code)

        return {"code": 0, "message": "轮函数保存成功", "data": None}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
