import { request, ApiResponse } from "./request";

// 保存bit matrix
export function bitMatrixSaveAPI(data: {}): Promise<ApiResponse<any>> {
  return request<any>({
    url: "sql/bit_matrix/save",
    method: "POST",
    data,
  });
}

// 获取所有bit matrix
export function bitMatrixGetAllAPI(skip: number, limit: number): Promise<ApiResponse<any[]>> {
  return request<any[]>({
    url: `sql/bit_matrix/list?skip=${skip}&limit=${limit}`,
    method: "GET",
  });
}

// 删除bit matrix
export function bitMatrixDeleteAPI(id: number): Promise<ApiResponse<any>> {
  return request<any>({
    url: `sql/bit_matrix/delete/${id}`,
    method: "GET",
  });
}

// 保存block matrix 
export function blockMatrixSaveAPI(data: {}): Promise<ApiResponse<any>> {
  return request<any>({
    url: "sql/block_matrix/save",
    method: "POST",
    data,
  });
}

// 获取所有block matrix 
export function blockMatrixGetAllAPI(skip: number, limit: number): Promise<ApiResponse<any[]>> {
  return request<any[]>({
    url: `sql/block_matrix/list?skip=${skip}&limit=${limit}`,
    method: "GET",
  });
}

// 删除block matrix 
export function blockMatrixDeleteAPI(id: number): Promise<ApiResponse<any>> {
  return request<any>({
    url: `sql/block_matrix/delete/${id}`,
    method: "GET",
  });
}

// 保存sbox
export function sboxSaveAPI(data: {}): Promise<ApiResponse<any>> {
  return request<any>({
    url: "sql/sbox/save",
    method: "POST",
    data,
  });
}

// 获取所有sbox
export function sboxGetAllAPI(skip: number, limit: number): Promise<ApiResponse<any[]>> {
  return request<any[]>({
    url: `sql/sbox/list?skip=${skip}&limit=${limit}`,
    method: "GET",
  });
}

// 删除sbox
export function sboxDeleteAPI(id: number): Promise<ApiResponse<any>> {
  return request<any>({
    url: `sql/sbox/delete/${id}`,
    method: "GET",
  });
}
