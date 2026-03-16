import { request, ApiResponse } from './request'

// 实现分析接口
export function implAnalyzeAPI(data: any): Promise<ApiResponse<any>> {
  console.log("🚀 implAnalyzeAPI 请求发送:", data)  // 调试打印
  return request<any>({
    url: '/impl_analyze/analyze',   // 注意这里对应后端 FastAPI 的路由
    method: 'POST',
    data,
  })
}
