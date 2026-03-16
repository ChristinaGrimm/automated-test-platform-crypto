from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/download/{file_name}")
async def download_file(file_name: str):
    """文件下载端点"""
    # 检查文件是否存在
    file_path = f"downloads/{file_name}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文件不存在")
    
    return FileResponse(
        file_path, 
        filename=file_name,
        media_type="application/octet-stream"
    )

    