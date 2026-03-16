from fastapi import APIRouter, HTTPException
from app.schemas import CheckStepTwoRequest, StandardResponse

router = APIRouter()

@router.post("/step_two", response_model=StandardResponse)
async def check_step_two(request: CheckStepTwoRequest):
    """检查第二步代码"""
    try:
        # 这里可以添加代码验证逻辑
        if not request.code.strip():
            return {"code": 1, "message": "代码不能为空"}
        
        return {"code": 0, "message": "验证通过"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

        

        