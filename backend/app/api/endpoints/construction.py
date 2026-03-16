from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.schemas import BlockMatrixRequest, BitMatrixRequest, SBoxRequest, StandardResponse
from app.utils.block_matrix_utils import construct_block_matrix
from app.utils.matrix_utils import construct_bit_matrix
from app.utils.sbox_utils import construct_sbox
from pydantic import BaseModel
import logging

# ✅ 引入全局缓存
from app.utils.analysis_manager import LATEST_CONSTRUCTION

# 配置日志
logger = logging.getLogger(__name__)

router = APIRouter()


def ensure_matrix(matrix):
    """
    确保返回值是二维 list。
    - 如果是 dict，取第一个 value。
    - 如果是 list of list，直接返回。
    - 如果是 list of int（1D），转成 Nx1 矩阵。
    - 如果是 int，说明不是矩阵，直接返回 None。
    """
    if isinstance(matrix, dict):
        matrix = list(matrix.values())[0] if matrix else []
    if isinstance(matrix, list):
        if all(isinstance(row, list) for row in matrix):  # 二维 list
            return matrix
        elif all(isinstance(x, int) for x in matrix):  # 一维数组 -> 转 Nx1 矩阵
            return [[x] for x in matrix]
    if isinstance(matrix, int):
        return None  # ❌ 跳过保存矩阵
    raise ValueError(f"ensure_matrix 出错: 不支持的矩阵格式 {type(matrix)}: {matrix}")



class BlockMatrixForm(BaseModel):
    block_size: str
    bit_size: str
    branch_number: str
    dr: str
    xor_count: str
    quantity: str

# 添加测试用的 GET 路由
@router.get("/block_matrix")
async def test_block_matrix():
    return {"message": "GET 请求成功，服务正常"}

# 添加 OPTIONS 请求处理 - 修正路径
@router.options("/block_matrix")
async def options_block_matrix():
    return JSONResponse(content={})

@router.post("/block_matrix", response_model=StandardResponse)
async def block_matrix_construction(request: BlockMatrixForm):
    """分块矩阵构造API"""
    try:
        # 验证参数
        if not all([request.block_size, request.bit_size, request.branch_number, 
                   request.dr, request.xor_count, request.quantity]):
            logger.error(f"参数不完整: {request.dict()}")
            return {
                "code": 1, 
                "message": "参数不完整，请提供所有必要参数",
                "data": None
            }

        # 验证参数范围
        block_size_int = int(request.block_size)
        bit_size_int = int(request.bit_size)
        
        if block_size_int not in [16, 32, 64]:
            return {"code": 4, "message": "分组大小必须是16、32或64比特", "data": None}
        
        if block_size_int % bit_size_int != 0:
            return {"code": 5, "message": "分组大小必须是分块大小的整数倍", "data": None}

        # 转换参数
        params = {
            "block_size": block_size_int,
            "bit_size": bit_size_int,
            "branch_number": int(request.branch_number),
            "dr": int(request.dr),
            "xor_count": int(request.xor_count),
            "quantity": int(request.quantity)
        }
        
        # 调用构造函数
        results = construct_block_matrix(params)
        
        if not results:
            return {"code": 2, "message": "未找到满足条件的矩阵", "data": None}
        
        # ✅ 取第一条结果，并确保是二维 list
        matrix = ensure_matrix(results[0])

        LATEST_CONSTRUCTION.clear()
        LATEST_CONSTRUCTION.update({
            "blockLength": block_size_int,
            "branchNumber": params["branch_number"],
            "bitPermutation": matrix,
            "linearMatrix": matrix,
            "sBoxLength": None,
            "sBoxContent": None,
            "nonLinearComponent": None,
        })

        return {"code": 0, "message": "构造成功", "data": {str(i): result for i, result in enumerate(results)}}
    except ValueError as e:
        return {"code": 3, "message": f"参数错误: {str(e)}", "data": None}
    except Exception as e:
        logger.error(f"构造过程中发生错误: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# 同样为其他路由添加 OPTIONS 处理
@router.options("/bit_matrix")
async def options_bit_matrix():
    return JSONResponse(content={})

@router.post("/bit_matrix", response_model=StandardResponse)
async def bit_matrix_construction(request: BitMatrixRequest):
    """比特矩阵构造API"""
    try:
        if not all([request.block_size, request.branch_number, request.depth, request.xor_count, request.quantity]):
            return {"code": 1, "message": "参数不完整，请提供所有必要参数", "data": None}
        
        results = construct_bit_matrix(request)
        if not results:
            return {"code": 2, "message": "未找到满足条件的矩阵", "data": None}

        # ✅ 确保矩阵是二维 list
        matrix = ensure_matrix(results[0])

        LATEST_CONSTRUCTION["bitPermutation"] = matrix
        LATEST_CONSTRUCTION["linearMatrix"] = matrix

        return {"code": 0, "message": "构造成功", "data": {str(i): result for i, result in enumerate(results)}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.options("/sbox")
async def options_sbox():
    return JSONResponse(content={})

# @router.post("/sbox", response_model=StandardResponse)
# async def sbox_construction(request: SBoxRequest):
#     """S盒构造API"""
#     try:
#         # results = construct_sbox(request)
#         # ✅ 把 Pydantic 模型转成字典
#         results = construct_sbox(request.dict())

#         # ✅ 保存 S 盒结果
#         # ✅ 保存 S 盒结果
#         if results:
#             # 尝试获取 S 盒长度，兼容不同字段
#             sbox_length = getattr(request, "sbox_size", None) \
#                         or getattr(request, "length", None) \
#                         or (len(results[0]) if results else None)

#             LATEST_CONSTRUCTION["sBoxLength"] = sbox_length
#             LATEST_CONSTRUCTION["sBoxContent"] = results[0]


#         return {"code": 0, "message": "构造成功", "data": {str(i): result for i, result in enumerate(results)}}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

@router.post("/sbox", response_model=StandardResponse)
async def sbox_construction(request: SBoxRequest):
    """S盒构造API"""
    try:
        results = construct_sbox(request.dict())

        if not results:
            return {
                "code": 1,
                "message": "S盒构造失败",
                "data": {}
            }

        sbox_length = len(results[0])
        first_sbox = results[0]

        # 保存
        LATEST_CONSTRUCTION["sBoxLength"] = sbox_length
        LATEST_CONSTRUCTION["sBoxContent"] = first_sbox

        # ⚠️ 保持前端 Object.values 能解析
        return {
            "code": 0,
            "message": "构造成功",
            "data": {str(i): result for i, result in enumerate(results)}
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
