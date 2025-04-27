import axios from 'axios'

const service = axios.create({
  baseURL: 'http://127.0.0.1:8000', // 指定Django后端端口8000
  timeout: 5000
})

// 请求拦截器
service.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`
  }
  return config
})

export default service