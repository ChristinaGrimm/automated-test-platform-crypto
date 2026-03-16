import { request, ApiResponse } from './request'

export function analyzeAPI(data: any): Promise<ApiResponse<any>> {
  console.log("🚀 analyzeAPI 请求发送:", data)  // ✅ 新增调试
  return request<any>({
    url: '/analyze',
    method: 'POST',
    data,
  })
}