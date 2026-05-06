import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000
})

// 系统API
export const getSystemStatus = () => api.get('/system/status')
export const getHealth = () => axios.get('/health')

// 大脑API
export const getBrains = () => api.get('/brains')
export const createBrain = (data: any) => api.post('/brains', data)
export const getBrain = (id: string) => api.get(`/brains/${id}`)
export const getBrainStatus = (id: string) => api.get(`/brains/${id}/status`)
export const executeBrainTask = (id: string, task: any) => api.post(`/brains/${id}/execute`, task)

// 代理API
export const getAgents = () => api.get('/agents')

// 任务API
export const getTasks = (status?: string) => api.get('/tasks', { params: { status } })
export const createTask = (data: any) => api.post('/tasks', data)

export default api
