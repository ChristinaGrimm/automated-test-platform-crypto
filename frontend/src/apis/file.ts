import { request, ApiResponse } from './request'

// 和后端保持一致
export interface SaveResponse {
  code: number
  msg: string
  filename: string
  path: string
}

// =================== 保存 ===================
export const saveBlockMatrixAPI = async (data: any): Promise<SaveResponse> => {
  const res: ApiResponse<SaveResponse> = await request<SaveResponse>({
    url: '/file/save/block_matrix/',
    method: 'POST',
    data,
  })
  // 关键：从 ApiResponse<T> 解包成 SaveResponse
  return res as unknown as SaveResponse
}

export const saveBitMatrixAPI = async (data: any): Promise<SaveResponse> => {
  const res: ApiResponse<SaveResponse> = await request<SaveResponse>({
    url: '/file/save/bit_matrix/',
    method: 'POST',
    data,
  })
  return res as unknown as SaveResponse
}

export const saveSboxAPI = async (data: any): Promise<SaveResponse> => {
  const res: ApiResponse<SaveResponse> = await request<SaveResponse>({
    url: '/file/save/sbox/',
    method: 'POST',
    data,
  })
  return res as unknown as SaveResponse
}

// =================== 下载 ===================
export const downloadFileAPI = async (filename: string): Promise<Blob> => {
  const res = await request<any>({
    url: `/file/download/${filename}`,
    method: 'GET',
    responseType: 'blob',
  })
  return res as unknown as Blob
}

