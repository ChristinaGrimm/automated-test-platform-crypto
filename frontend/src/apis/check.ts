import { request, ApiResponse } from "./request";

export function checkStepOneAPI(data: {}): Promise<ApiResponse<any>> {
  return request<any>({
    url: "v1/check/step1",
    method: "POST",
    data,
  });
}

export function checkStepTwoAPI(data: {}): Promise<ApiResponse<any>> {
  return request<any>({
    url: "v1/check/step2",
    method: "POST",
    data,
  });
}
