import { request, ApiResponse } from "./request";

// 提交完整的算法设计
export function submitAlgorithmDesignAPI(data: {
  round_function: string;
  algorithm_structure: string;
  key_schedule: string;
}): Promise<ApiResponse<any>> {
  return request<any>({
    url: "/algorithm/design",
    method: "POST",
    data,
  });
}

// 获取支持的算法结构列表
export function getAlgorithmStructuresAPI(): Promise<ApiResponse<any[]>> {
  return request<any[]>({
    url: "/algorithm/structures",
    method: "GET",
  });
}

// 验证算法代码语法
export function validateAlgorithmCodeAPI(data: { code: string; type: string }): Promise<ApiResponse<any>> {
  return request<any>({
    url: "/algorithm/validate",
    method: "POST",
    data,
  });
}

// 获取算法设计历史
export function getAlgorithmHistoryAPI(): Promise<ApiResponse<any[]>> {
  return request<any[]>({
    url: "/algorithm/history",
    method: "GET",
  });
}

// 删除算法设计
export function deleteAlgorithmDesignAPI(id: number): Promise<ApiResponse<any>> {
  return request<any>({
    url: `/algorithm/design/${id}`,
    method: "DELETE",
  });
}

// algorithm.ts (追加)
export function saveRoundFunctionAPI(data: { code: string }): Promise<ApiResponse<any>> {
  return request<any>({
    url: "/algorithm/save_round_function",
    method: "POST",
    data,
  });
}

