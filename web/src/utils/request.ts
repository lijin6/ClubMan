// /@/utils/request.js
import axios from 'axios';

const service = axios.create({
  baseURL: 'http://localhost:8000', // 你的后端 API 地址
  timeout: 5000, // 请求超时时间
});

// 请求拦截器
service.interceptors.request.use(
  (config) => {
    // 在发送请求之前做些什么
    return config;
  },
  (error) => {
    // 对请求错误做些什么
    console.log(error);
    return Promise.reject(error);
  },
);

// 响应拦截器
service.interceptors.response.use(
  (response) => {
    // 对响应数据做点什么
    return response.data;
  },
  (error) => {
    // 对响应错误做点什么
    console.log(error);
    return Promise.reject(error);
  },
);

export default service;
