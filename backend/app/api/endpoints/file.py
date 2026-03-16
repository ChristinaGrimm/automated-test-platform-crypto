import os
import json
import datetime
from fastapi import APIRouter
from fastapi.responses import FileResponse

# 固定保存目录
RESULT_DIR = "/home/lys/projects/automated_design/backend/app/utils/analysis/result"
os.makedirs(RESULT_DIR, exist_ok=True)

router = APIRouter()


def write_txt(filename: str, data: dict):
    """写入 txt 文件"""
    filepath = os.path.join(RESULT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(json.dumps(data, indent=2, ensure_ascii=False))
    return filepath


@router.post("/save/block_matrix/")
async def save_block_matrix(data: dict):
    filename = f"block_matrix_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
    filepath = write_txt(filename, data)
    return {"code": 0, "msg": "分块阵保存成功", "filename": filename, "path": filepath}


@router.post("/save/bit_matrix/")
async def save_bit_matrix(data: dict):
    filename = f"bit_matrix_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
    filepath = write_txt(filename, data)
    return {"code": 0, "msg": "比特阵保存成功", "filename": filename, "path": filepath}


@router.post("/save/sbox/")
async def save_sbox(data: dict):
    filename = f"sbox_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
    filepath = write_txt(filename, data)
    return {"code": 0, "msg": "S盒保存成功", "filename": filename, "path": filepath}


@router.get("/download/{filename}")
async def download(filename: str):
    filepath = os.path.join(RESULT_DIR, filename)
    if os.path.exists(filepath):
        return FileResponse(filepath, filename=filename, media_type="text/plain")
    return {"code": 1, "msg": "文件不存在"}
