from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class BlockMatrixRequest(BaseModel):
    block_size: Optional[int] = None
    bit_size: Optional[int] = None
    branch_number: Optional[int] = None
    dr: Optional[int] = None
    xor_count: Optional[int] = None
    quantity: Optional[int] = None

class BitMatrixRequest(BaseModel):
    block_size: Optional[int] = None
    branch_number: Optional[int] = None
    depth: Optional[int] = None
    xor_count: Optional[int] = None
    quantity: Optional[int] = None

class SBoxRequest(BaseModel):
    bit_num: Optional[int] = None
    diff_uniform: Optional[int] = None
    linear_uniform: Optional[int] = None
    dbn: Optional[int] = None
    lbn: Optional[int] = None
    bibo_ddt: Optional[int] = None
    bibo_lat: Optional[int] = None
    quantity: Optional[int] = None

class BitMatrixSaveRequest(BaseModel):
    dimension: int
    branch_number: int
    depth: Optional[int] = None
    xor_count: int
    matrix: str
    add_time: str

class SBoxSaveRequest(BaseModel):
    sbox: str
    add_time: str

class CheckStepTwoRequest(BaseModel):
    code: str
    analyzeType: Optional[str] = None

class AnalyzeRequest(BaseModel):
    # 第一步可能存在的构造结果（全部设为 Optional）
    blockLength: Optional[int] = None
    branchNumber: Optional[int] = None
    bitPermutation: Optional[Any] = None
    linearMatrix: Optional[Any] = None
    sBoxLength: Optional[int] = None
    sBoxContent: Optional[Any] = None
    nonLinearComponent: Optional[Any] = None
    code: Optional[str] = ""      # 轮函数代码，第二步输入；可选空串
    analyzeType: str             # 必选，分析类型 (dc, lc, ic, idc, zlc)

# class StandardResponse(BaseModel):
#     code: int
#     message: str
#     data: Optional[Dict[str, Any]] = None

class StandardResponse(BaseModel):
    code: int
    message: str
    data: Optional[Any] = None

class AlgorithmDesignRequest(BaseModel):
    round_function: str
    key_schedule: str

class CodeValidationRequest(BaseModel):
    code: str
    type: str  # 'round_function' 或 'key_schedule'

class RoundFunctionSaveRequest(BaseModel):
    code: str

