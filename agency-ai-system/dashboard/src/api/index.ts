import axios from 'axios'

const http = axios.create({
  baseURL: '/api',
  timeout: 10000
})

// 请求拦截器
http.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
http.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    console.error('API请求错误:', error)
    return Promise.reject(error)
  }
)

// 系统API
export const getSystemStatus = () => http.get('/system/status')

// 任务API
export const getTasks = (status?: string) => http.get('/tasks', { params: { status } })
export const getTask = (id: string) => http.get(`/tasks/${id}`)
export const createTask = (data: any) => http.post('/tasks', data)
export const cancelTask = (id: string) => http.post(`/tasks/${id}/cancel`)

// 代理API
export const getAgents = () => http.get('/agents')
export const getAgent = (id: string) => http.get(`/agents/${id}`)
export const createAgent = (data: any) => http.post('/agents', data)
export const updateAgent = (id: string, data: any) => http.put(`/agents/${id}`, data)
export const toggleAgent = (id: string) => http.post(`/agents/${id}/toggle`)

// 大脑API
export const getBrains = () => http.get('/brains')
export const getBrain = (id: string) => http.get(`/brains/${id}`)
export const createBrain = (data: any) => http.post('/brains', data)
export const updateBrain = (id: string, data: any) => http.put(`/brains/${id}`, data)

// 模型API
export const getModels = () => http.get('/models')
export const createModel = (data: any) => http.post('/models', data)
export const updateModel = (id: string, data: any) => http.put(`/models/${id}`, data)

// 日志API
export const getLogs = (params?: any) => http.get('/logs', { params })
export const getRecentLogs = (limit?: number) => http.get('/logs/recent', { params: { limit } })
export const getLogsByCategory = (category: string) => http.get(`/logs/category/${category}`)
export const getErrorLogs = () => http.get('/logs/errors')
export const getLogStatistics = () => http.get('/logs/statistics')
export const searchLogs = (keyword: string) => http.get('/logs/search', { params: { keyword } })
export const getLogTimeline = (hours?: number) => http.get('/logs/timeline', { params: { hours } })
export const getLogSummary = () => http.get('/logs/summary')

// 健康检查
export const getHealthCheck = () => http.get('/heartbeat/health')

// 进度监控
export const getProgressReport = () => http.get('/progress/report')
export const getProgressStatus = () => http.get('/progress/status')

export default {
  getSystemStatus,
  getTasks,
  getTask,
  createTask,
  cancelTask,
  getAgents,
  getAgent,
  createAgent,
  updateAgent,
  toggleAgent,
  getBrains,
  getBrain,
  createBrain,
  updateBrain,
  getModels,
  createModel,
  updateModel,
  getLogs,
  getRecentLogs,
  getLogsByCategory,
  getErrorLogs,
  getLogStatistics,
  searchLogs,
  getLogTimeline,
  getLogSummary,
  getHealthCheck,
  getProgressReport,
  getProgressStatus
}
