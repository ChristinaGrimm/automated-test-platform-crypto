import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from itertools import combinations

import logging

logger = logging.getLogger(__name__)
np.set_printoptions(threshold=np.inf, linewidth=np.inf)

class SubSquareMatrix:
    def __init__(self, dimension, bit_size, matrix):
        self.bit_size = bit_size
        self.dimension = dimension
        self.matrix = matrix
        self.shape = dimension * bit_size

    def get_1_1_sub_matrices(self):
        matrix = self.matrix
        bit = self.bit_size
        shape = self.shape
        sub_matrix = [
            matrix[i : i + bit, j : j + bit]
            for i in range(0, shape, bit)
            for j in range(0, shape, bit)
        ]
        return sub_matrix

    def get_2_2_sub_matrices(self):
        matrix = self.matrix
        bit = self.bit_size
        shape = self.shape
        sub_matrix = [
            [
                [
                    matrix[i : i + bit, p : p + bit],
                    matrix[i : i + bit, q : q + bit],
                ],
                [
                    matrix[j : j + bit, p : p + bit],
                    matrix[j : j + bit, q : q + bit],
                ],
            ]
            for i in range(0, shape - bit, bit)
            for j in range(i + bit, shape, bit)
            for p in range(0, shape - bit, bit)
            for q in range(p + bit, shape, bit)
        ]
        return sub_matrix

    def get_3_3_sub_matrices(self):
        matrix = self.matrix
        bit = self.bit_size
        shape = self.shape
        sub_matrix = [
            [
                [
                    matrix[i : i + bit, p : p + bit],
                    matrix[i : i + bit, q : q + bit],
                    matrix[i : i + bit, r : r + bit],
                ],
                [
                    matrix[j : j + bit, p : p + bit],
                    matrix[j : j + bit, q : q + bit],
                    matrix[j : j + bit, r : r + bit],
                ],
                [
                    matrix[k : k + bit, p : p + bit],
                    matrix[k : k + bit, q : q + bit],
                    matrix[k : k + bit, r : r + bit],
                ],
            ]
            for i in range(0, shape - 2 * bit, bit)
            for j in range(i + bit, shape - bit, bit)
            for k in range(j + bit, shape, bit)
            for p in range(0, shape - 2 * bit, bit)
            for q in range(p + bit, shape - bit, bit)
            for r in range(q + bit, shape, bit)
        ]
        return sub_matrix

    def get_4_4_sub_matrices(self):
        matrix = self.matrix
        bit = self.bit_size
        shape = self.shape
        sub_matrix = [
            [
                [
                    matrix[i : i + bit, p : p + bit],
                    matrix[i : i + bit, q : q + bit],
                    matrix[i : i + bit, r : r + bit],
                    matrix[i : i + bit, s : s + bit],
                ],
                [
                    matrix[j : j + bit, p : p + bit],
                    matrix[j : j + bit, q : q + bit],
                    matrix[j : j + bit, r : r + bit],
                    matrix[j : j + bit, s : s + bit],
                ],
                [
                    matrix[k : k + bit, p : p + bit],
                    matrix[k : k + bit, q : q + bit],
                    matrix[k : k + bit, r : r + bit],
                    matrix[k : k + bit, s : s + bit],
                ],
                [
                    matrix[l : l + bit, p : p + bit],
                    matrix[l : l + bit, q : q + bit],
                    matrix[l : l + bit, r : r + bit],
                    matrix[l : l + bit, s : s + bit],
                ],
            ]
            for i in range(0, shape - 3 * bit, bit)
            for j in range(i + bit, shape - 2 * bit, bit)
            for k in range(j + bit, shape - bit, bit)
            for l in range(k + bit, shape, bit)
            for p in range(0, shape - 3 * bit, bit)
            for q in range(p + bit, shape - 2 * bit, bit)
            for r in range(q + bit, shape - bit, bit)
            for s in range(r + bit, shape, bit)
        ]
        return sub_matrix

    def get_5_5_sub_matrices(self):
        matrix = self.matrix
        bit = self.bit_size
        shape = self.shape
        sub_matrix = [
            [
                [
                    matrix[i : i + bit, p : p + bit],
                    matrix[i : i + bit, q : q + bit],
                    matrix[i : i + bit, r : r + bit],
                    matrix[i : i + bit, s : s + bit],
                    matrix[i : i + bit, t : t + bit],
                ],
                [
                    matrix[j : j + bit, p : p + bit],
                    matrix[j : j + bit, q : q + bit],
                    matrix[j : j + bit, r : r + bit],
                    matrix[j : j + bit, s : s + bit],
                    matrix[j : j + bit, t : t + bit],
                ],
                [
                    matrix[k : k + bit, p : p + bit],
                    matrix[k : k + bit, q : q + bit],
                    matrix[k : k + bit, r : r + bit],
                    matrix[k : k + bit, s : s + bit],
                    matrix[k : k + bit, t : t + bit],
                ],
                [
                    matrix[l : l + bit, p : p + bit],
                    matrix[l : l + bit, q : q + bit],
                    matrix[l : l + bit, r : r + bit],
                    matrix[l : l + bit, s : s + bit],
                    matrix[l : l + bit, t : t + bit],
                ],
                [
                    matrix[m : m + bit, p : p + bit],
                    matrix[m : m + bit, q : q + bit],
                    matrix[m : m + bit, r : r + bit],
                    matrix[m : m + bit, s : s + bit],
                    matrix[m : m + bit, t : t + bit],
                ],
            ]
            for i in range(0, shape - 4 * bit, bit)
            for j in range(i + bit, shape - 3 * bit, bit)
            for k in range(j + bit, shape - 2 * bit, bit)
            for l in range(k + bit, shape - bit, bit)
            for m in range(l + bit, shape, bit)
            for p in range(0, shape - 4 * bit, bit)
            for q in range(p + bit, shape - 3 * bit, bit)
            for r in range(q + bit, shape - 2 * bit, bit)
            for s in range(r + bit, shape - bit, bit)
            for t in range(s + bit, shape, bit)
        ]
        return sub_matrix

    def get_6_6_sub_matrices(self):
        matrix = self.matrix
        bit = self.bit_size
        shape = self.shape
        sub_matrix = [
            [
                [
                    matrix[i : i + bit, p : p + bit],
                    matrix[i : i + bit, q : q + bit],
                    matrix[i : i + bit, r : r + bit],
                    matrix[i : i + bit, s : s + bit],
                    matrix[i : i + bit, t : t + bit],
                    matrix[i : i + bit, u : u + bit],
                ],
                [
                    matrix[j : j + bit, p : p + bit],
                    matrix[j : j + bit, q : q + bit],
                    matrix[j : j + bit, r : r + bit],
                    matrix[j : j + bit, s : s + bit],
                    matrix[j : j + bit, t : t + bit],
                    matrix[j : j + bit, u : u + bit],
                ],
                [
                    matrix[k : k + bit, p : p + bit],
                    matrix[k : k + bit, q : q + bit],
                    matrix[k : k + bit, r : r + bit],
                    matrix[k : k + bit, s : s + bit],
                    matrix[k : k + bit, t : t + bit],
                    matrix[k : k + bit, u : u + bit],
                ],
                [
                    matrix[l : l + bit, p : p + bit],
                    matrix[l : l + bit, q : q + bit],
                    matrix[l : l + bit, r : r + bit],
                    matrix[l : l + bit, s : s + bit],
                    matrix[l : l + bit, t : t + bit],
                    matrix[l : l + bit, u : u + bit],
                ],
                [
                    matrix[m : m + bit, p : p + bit],
                    matrix[m : m + bit, q : q + bit],
                    matrix[m : m + bit, r : r + bit],
                    matrix[m : m + bit, s : s + bit],
                    matrix[m : m + bit, t : t + bit],
                    matrix[m : m + bit, u : u + bit],
                ],
                [
                    matrix[n : n + bit, p : p + bit],
                    matrix[n : n + bit, q : q + bit],
                    matrix[n : n + bit, r : r + bit],
                    matrix[n : n + bit, s : s + bit],
                    matrix[n : n + bit, t : t + bit],
                    matrix[n : n + bit, u : u + bit],
                ],
            ]
            for i in range(0, shape - 5 * bit, bit)
            for j in range(i + bit, shape - 4 * bit, bit)
            for k in range(j + bit, shape - 3 * bit, bit)
            for l in range(k + bit, shape - 2 * bit, bit)
            for m in range(l + bit, shape - bit, bit)
            for n in range(m + bit, shape, bit)
            for p in range(0, shape - 5 * bit, bit)
            for q in range(p + bit, shape - 4 * bit, bit)
            for r in range(q + bit, shape - 3 * bit, bit)
            for s in range(r + bit, shape - 2 * bit, bit)
            for t in range(s + bit, shape - bit, bit)
            for u in range(t + bit, shape, bit)
        ]
        return sub_matrix

    def get_7_7_sub_matrices(self):
        matrix = self.matrix
        bit = self.bit_size
        shape = self.shape
        sub_matrix = [
            [
                [
                    matrix[i : i + bit, p : p + bit],
                    matrix[i : i + bit, q : q + bit],
                    matrix[i : i + bit, r : r + bit],
                    matrix[i : i + bit, s : s + bit],
                    matrix[i : i + bit, t : t + bit],
                    matrix[i : i + bit, u : u + bit],
                    matrix[i : i + bit, v : v + bit],
                ],
                [
                    matrix[j : j + bit, p : p + bit],
                    matrix[j : j + bit, q : q + bit],
                    matrix[j : j + bit, r : r + bit],
                    matrix[j : j + bit, s : s + bit],
                    matrix[j : j + bit, t : t + bit],
                    matrix[j : j + bit, u : u + bit],
                    matrix[j : j + bit, v : v + bit],
                ],
                [
                    matrix[k : k + bit, p : p + bit],
                    matrix[k : k + bit, q : q + bit],
                    matrix[k : k + bit, r : r + bit],
                    matrix[k : k + bit, s : s + bit],
                    matrix[k : k + bit, t : t + bit],
                    matrix[k : k + bit, u : u + bit],
                    matrix[k : k + bit, v : v + bit],
                ],
                [
                    matrix[l : l + bit, p : p + bit],
                    matrix[l : l + bit, q : q + bit],
                    matrix[l : l + bit, r : r + bit],
                    matrix[l : l + bit, s : s + bit],
                    matrix[l : l + bit, t : t + bit],
                    matrix[l : l + bit, u : u + bit],
                    matrix[l : l + bit, v : v + bit],
                ],
                [
                    matrix[m : m + bit, p : p + bit],
                    matrix[m : m + bit, q : q + bit],
                    matrix[m : m + bit, r : r + bit],
                    matrix[m : m + bit, s : s + bit],
                    matrix[m : m + bit, t : t + bit],
                    matrix[m : m + bit, u : u + bit],
                    matrix[m : m + bit, v : v + bit],
                ],
                [
                    matrix[n : n + bit, p : p + bit],
                    matrix[n : n + bit, q : q + bit],
                    matrix[n : n + bit, r : r + bit],
                    matrix[n : n + bit, s : s + bit],
                    matrix[n : n + bit, t : t + bit],
                    matrix[n : n + bit, u : u + bit],
                    matrix[n : n + bit, v : v + bit],
                ],
                [
                    matrix[o : o + bit, p : p + bit],
                    matrix[o : o + bit, q : q + bit],
                    matrix[o : o + bit, r : r + bit],
                    matrix[o : o + bit, s : s + bit],
                    matrix[o : o + bit, t : t + bit],
                    matrix[o : o + bit, u : u + bit],
                    matrix[o : o + bit, v : v + bit],
                ],
            ]
            for i in range(0, shape - 6 * bit, bit)
            for j in range(i + bit, shape - 5 * bit, bit)
            for k in range(j + bit, shape - 4 * bit, bit)
            for l in range(k + bit, shape - 3 * bit, bit)
            for m in range(l + bit, shape - 2 * bit, bit)
            for n in range(m + bit, shape - bit, bit)
            for o in range(n + bit, shape, bit)
            for p in range(0, shape - 6 * bit, bit)
            for q in range(p + bit, shape - 5 * bit, bit)
            for r in range(q + bit, shape - 4 * bit, bit)
            for s in range(r + bit, shape - 3 * bit, bit)
            for t in range(s + bit, shape - 2 * bit, bit)
            for u in range(t + bit, shape - bit, bit)
            for v in range(u + bit, shape, bit)
        ]
        return sub_matrix

    def get_all_sub_matrices(self):
        n = self.dimension
        all_sub_matrices = []
        if n == 8:
            all_sub_matrices = (
                self.get_1_1_sub_matrices()
                + self.get_2_2_sub_matrices()
                + self.get_3_3_sub_matrices()
                + self.get_4_4_sub_matrices()
                + self.get_5_5_sub_matrices()
                + self.get_6_6_sub_matrices()
                + self.get_7_7_sub_matrices()
                + [self.matrix]
            )
        elif n == 6:
            all_sub_matrices = (
                self.get_1_1_sub_matrices()
                + self.get_2_2_sub_matrices()
                + self.get_3_3_sub_matrices()
                + self.get_4_4_sub_matrices()
                + self.get_5_5_sub_matrices()
                + self.get_6_6_sub_matrices()
                + [self.matrix]
            )
        elif n == 4:
            all_sub_matrices = (
                self.get_1_1_sub_matrices()
                + self.get_2_2_sub_matrices()
                + self.get_3_3_sub_matrices()
                + [self.matrix]
            )
        return [np.block(block) for block in all_sub_matrices]


def validate_block_matrix_params(block_size: int, bit_size: int) -> bool:
    """验证分块矩阵参数是否有效"""
    if block_size % bit_size != 0:
        return False
    
    dimension = block_size // bit_size
    if dimension not in [4, 8]:
        return False
    
    return True

def format_matrix_for_display(matrix: List[List[int]], block_size: int) -> str:
    """格式化矩阵用于显示"""
    nrows = len(matrix)
    ncols = len(matrix[0]) if nrows > 0 else 0
    output = ""
    
    for row in range(nrows):
        if row % block_size == 0 and row != 0:
            output += "-" * (block_size * 2)
            output += ("+" + "-" * (block_size * 2 + 1)) * (ncols // block_size - 2)
            output += "+" + "-" * (block_size * 2) + "\n"
        for col in range(ncols):
            if col % block_size == 0 and col != 0:
                output += "| "
            output += f"{matrix[row][col]:d} "
        output = output.strip() + "\n"
    
    return output


def matrix_power(matrix, n):
    if n == 0:
        return np.identity(len(matrix), dtype=np.int8)
    elif n < 0:
        res = np.array(np.linalg.inv(matrix) % 2, dtype=np.int8)
        return np.linalg.matrix_power(res, -n) % 2
    else:
        return np.linalg.matrix_power(matrix, n) % 2


def det(matrix):
    row = matrix.shape[0]
    for i in range(row):
        non_zero_row = np.argmax(matrix[i:, i]) + i
        if matrix[non_zero_row, i] == 0:
            return 0
        matrix[[i, non_zero_row]] = matrix[[non_zero_row, i]]
        for j in range(i + 1, row):
            if matrix[j, i] == 1:
                matrix[j] = np.bitwise_xor(matrix[j], matrix[i])
    return 1


def generate_L(size: int, n: int) -> list:
    all_L = []
    L = np.eye(size, dtype=np.int8)
    L = np.roll(L, -1, axis=1)
    if n == 2:
        L[0][0] = 1
        L[0][1] = 1
        n -= 1

    zero_indices = np.transpose(np.where(L == 0))
    zero_comb = combinations(zero_indices, n)
    for i in zero_comb:
        for j in i:
            L[j[0]][j[1]] = 1
        if det(L.copy()) != 0:
            all_L.append(L.copy())
        for j in i:
            L[j[0]][j[1]] = 0
    return all_L


def is_mds(matrix, bit_size, dimension):
    M = SubSquareMatrix(dimension, bit_size, matrix)
    sub_matrix = M.get_all_sub_matrices()
    for a in sub_matrix:
        if det(a) == 0:
            return False
    return True


def calc_diffusion_round(matrix):
    size = len(matrix)
    dr = 0
    for i in range(1, size + 1):
        if (
            np.count_nonzero(np.linalg.matrix_power(np.array(matrix.tolist()), i))
            == size**2
        ):
            dr = i
            break
    return dr


def format_block_matrix(matrix, block_size):
    nrows, ncols = matrix.shape
    output = ""
    for row in range(nrows):
        if row % block_size == 0 and row != 0:
            output += "-" * (block_size * 2)
            output += ("+" + "-" * (block_size * 2 + 1)) * (ncols // block_size - 2)
            output += "+" + "-" * (block_size * 2) + "\n"
        for col in range(ncols):
            if col % block_size == 0 and col != 0:
                output += "| "
            output += f"{matrix[row, col]:d} "
        output = output.strip() + "\n"
    return output


def LFSR_matrix(dimension, L, identity, zero):
    if dimension == 4:
        l1, l2, l3, l4 = L
        A = np.block(
            [
                [zero, identity, zero, zero],
                [zero, zero, identity, zero],
                [zero, zero, zero, identity],
                [l1, l2, l3, l4],
            ]
        )
        matrix = matrix_power(A, 4)
    else:
        l1, l2, l3, l4, l5, l6, l7, l8 = L
        A = np.block(
            [
                [zero, identity, zero, zero, zero, zero, zero, zero],
                [zero, zero, identity, zero, zero, zero, zero, zero],
                [zero, zero, zero, identity, zero, zero, zero, zero],
                [zero, zero, zero, zero, identity, zero, zero, zero],
                [zero, zero, zero, zero, zero, identity, zero, zero],
                [zero, zero, zero, zero, zero, zero, identity, zero],
                [zero, zero, zero, zero, zero, zero, zero, identity],
                [l1, l2, l3, l4, l5, l6, l7, l8],
            ]
        )
        matrix = matrix_power(A, 8)
    return matrix


def calculate_cost(dimension, L, n):
    cost = 0
    for l in L:
        cost += np.count_nonzero(l) - n
    if dimension == 4:
        cost += 3 * n
        cost *= 4
    else:
        cost += 7 * n
        cost *= 8
    return cost


def search_LFSR_MDS(block_size: int, bitsize: int, dr_0: int, xor_count: int, quantity: int) -> List[Dict[str, Any]]:
    dimension = int(block_size / bitsize)
    cnt = 1
    result = []
    L = generate_L(bitsize, 1)
    identity = np.identity(bitsize, dtype=np.int8)
    zero = np.zeros((bitsize, bitsize), dtype=np.int8)
    
    if dimension == 4:
        for l in L:
            ll = (l, identity, identity, matrix_power(l, 2))
            matrix = LFSR_matrix(dimension, ll, identity, zero)
            matrix1 = matrix.copy()
            res1 = is_mds(matrix1, bitsize, 4)
            if res1:
                dr = calc_diffusion_round(matrix1)
                cost = calculate_cost(dimension, ll, bitsize)
                if dr > dr_0:
                    continue
                if cost > xor_count:
                    continue
                
                res = {
                    "dr": dr,
                    "cost": cost,
                    "block_size": 4 * bitsize,
                    "bit_size": bitsize,
                    "matrix": matrix1.tolist(),
                    "branch_number": 5
                }
                result.append(res)
                cnt += 1
                if cnt > quantity:
                    break
    else:
        for l in L:
            ll = (
                identity,
                matrix_power(l, -3),
                l,
                matrix_power(l, 3),
                matrix_power(l, 2),
                matrix_power(l, 3),
                l,
                matrix_power(l, -3),
            )
            matrix = LFSR_matrix(dimension, ll, identity, zero)
            res1 = is_mds(matrix, bitsize, 8)
            if res1:
                dr = calc_diffusion_round(matrix)
                cost = calculate_cost(dimension, ll, bitsize)
                if dr > dr_0:
                    continue
                if cost > xor_count:
                    continue
                
                res = {
                    "dr": dr,
                    "cost": cost,
                    "block_size": 8 * bitsize,
                    "bit_size": bitsize,
                    "matrix": matrix.tolist(),
                    "branch_number": 9
                }
                result.append(res)
                cnt += 1
                if cnt > quantity:
                    break
    return result


def construct_block_matrix(params: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    构造分块矩阵的主函数
    
    参数:
        params: 包含构造参数的字典，应包括:
            block_size: 分组大小(比特)
            bit_size: 分块大小(比特)
            branch_number: 分支数
            dr: 全扩散次数上界
            xor_count: 异或数上界
            quantity: 数量
    
    返回:
        包含构造结果的列表，每个结果是一个字典
    """
    try:
        # logger.info(f"接收到构造参数: {params}")

        block_size = params.get("block_size")
        bit_size = params.get("bit_size")
        dr = params.get("dr")
        xor_count = params.get("xor_count")
        quantity = params.get("quantity")
        
        # 验证参数
        if not all([block_size, bit_size, dr, xor_count, quantity]):
            logger.error("缺少必要的构造参数")
            raise ValueError("缺少必要的构造参数")
        
        if block_size % bit_size != 0:
            logger.error(f"分组大小 {block_size} 不是分块大小 {bit_size} 的整数倍")
            raise ValueError("分组大小必须是分块大小的整数倍")
        
        dimension = block_size // bit_size
        if dimension not in [4, 8]:
            logger.error(f"不支持的分块维度: {dimension}")
            raise ValueError("只支持4x4和8x8的分块矩阵")
        
        logger.info(f"开始构造分块矩阵: block_size={block_size}, bit_size={bit_size}, "
                   f"dr={dr}, xor_count={xor_count}, quantity={quantity}")
        
        # 调用搜索函数
        results = search_LFSR_MDS(block_size, bit_size, dr, xor_count, quantity)
        
        logger.info(f"分块矩阵构造完成，找到 {len(results)} 个结果")
        
        return results
        
    except Exception as e:
        logger.error(f"分块矩阵构造过程中发生错误: {str(e)}")
        raise