from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

# 请求体模型
class ImplForm(BaseModel):
    blockLength: Optional[int] = None
    subKeyLength: Optional[int] = None
    roundSboxCount: Optional[int] = None
    keySboxCount: Optional[int] = None
    roundModuloCount: Optional[int] = None
    keyModuloCount: Optional[int] = None
    roundXorCount: Optional[int] = None
    keyXorCount: Optional[int] = None

@router.post("/analyze")
def impl_analyze(form: ImplForm):
    # 取值，没选的默认 0
    block_len = form.blockLength or 0
    subkey_len = form.subKeyLength or 0

    sbox_total = (form.roundSboxCount or 0) + (form.keySboxCount or 0)
    modulo_total = (form.roundModuloCount or 0) + (form.keyModuloCount or 0)
    xor_total = (form.roundXorCount or 0) + (form.keyXorCount or 0)

    # 计算公式
    result = (block_len + subkey_len) * 6.25 + sbox_total * 12.33 + modulo_total * 347 + xor_total * 3

    return {
        "code": 0,
        "message": "实现分析成功",
        "data": {
            "implResult": round(result, 2)  # 保留两位小数
        }
    }
