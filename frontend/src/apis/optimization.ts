import { request, ApiResponse } from "./request";

export function saveMatrix(data: any): Promise<ApiResponse<any>> {
  return request<any>({
    url: "/optimization/matrix",
    method: "POST",
    data,
  });
}

export function optimizeSboxApi(data: {}): Promise<ApiResponse<any>> {
  return request<any>({
    url: "/optimization/sbox",
    method: "POST",
    data,
  });
}
