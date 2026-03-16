import { request, ApiResponse } from "./request";

export function adminLoginAPI(data: {}): Promise<ApiResponse<any>> {
  return request<any>({
    url: "/admin/login",
    method: "POST",
    data,
  });
}

export function getAdminInfoAPI(): Promise<ApiResponse<any>> {
  return request<any>({
    url: "/admin/info",
    method: "GET",
  });
}
