import { request, ApiResponse } from './request'

// 分块矩阵构造
export function blockMatrixConstructionAPI(
  data: any
): Promise<ApiResponse<{ [key: string]: any }>> {
  return request<{ [key: string]: any }>({
    url: '/construction/block_matrix',
    method: 'POST',
    data,
  })
}

// 比特矩阵构造
export function bitMatrixConstructionAPI(
  data: any
): Promise<ApiResponse<any[]>> {
  return request<any[]>({
    url: '/construction/bit_matrix',
    method: 'POST',
    data,
  })
}

// S盒构造
export function sboxConstructionAPI(
  data: any
): Promise<ApiResponse<any[]>> {
  return request<any[]>({
    url: '/construction/sbox',
    method: 'POST',
    data,
  })
}
