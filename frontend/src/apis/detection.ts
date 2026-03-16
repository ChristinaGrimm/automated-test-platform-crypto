import { request, ApiResponse } from "./request";

export function sboxPropsDetectionAPI(data: {}): Promise<ApiResponse<any>> {
  return request<any>({
    url: "/detection/sbox_props",
    method: "POST",
    data,
  });
}

export function FFMatrixDetectionAPI(data: {}): Promise<ApiResponse<any>> {
  return request<any>({
    url: "/detection/finite_field_matrix",
    method: "POST",
    data,
  });
}

export function blockMatrixDetectionAPI(data: {}): Promise<ApiResponse<any>> {
  return request<any>({
    url: "/detection/block_matrix",
    method: "POST",
    data,
  });
}
