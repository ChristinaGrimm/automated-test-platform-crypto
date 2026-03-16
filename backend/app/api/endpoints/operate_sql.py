from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import BitMatrixSaveRequest, SBoxSaveRequest, StandardResponse
from app.database import get_db
from app.models import BitMatrix, SBox
from datetime import datetime

router = APIRouter()

@router.post("/bit_matrix_save", response_model=StandardResponse)
async def bit_matrix_save(request: BitMatrixSaveRequest, db: Session = Depends(get_db)):
    """保存比特矩阵到数据库"""
    try:
        db_matrix = BitMatrix(
            dimension=request.dimension,
            branch_number=request.branch_number,
            depth=request.depth,
            xor_count=request.xor_count,
            matrix=request.matrix,
            add_time=datetime.strptime(request.add_time, "%Y-%m-%d %H:%M:%S")
        )
        db.add(db_matrix)
        db.commit()
        return {"code": 0, "message": "保存成功"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/sbox_save", response_model=StandardResponse)
async def sbox_save(request: SBoxSaveRequest, db: Session = Depends(get_db)):
    """保存S盒到数据库"""
    try:
        db_sbox = SBox(
            sbox=request.sbox,
            add_time=datetime.strptime(request.add_time, "%Y-%m-%d %H:%M:%S")
        )
        db.add(db_sbox)
        db.commit()
        return {"code": 0, "message": "保存成功"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

        