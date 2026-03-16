import axios, { AxiosInstance, AxiosRequestConfig } from 'axios'
import { storageData as storage } from "@/utils/stored-data"

// 通用 API 响应结构
export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

const service: AxiosInstance = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

// 请求拦截器
service.interceptors.request.use(
  (config) => {
    const token = storage.get("access_token");
    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }
    config.headers["Accept"] = "application/json";
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
service.interceptors.response.use(
  (response) => {
    return response.data; // 直接返回 data，调用时就是 res.code / res.data.xxx
  },
  (error) => {
    return Promise.reject(error);
  }
);


// 封装一个带泛型的请求方法
export function request<T = any>(config: AxiosRequestConfig) {
  return service.request<any, ApiResponse<T>>(config)
}

export default request
