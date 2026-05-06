export interface Brain {
  id: string
  name: string
  brain_type: string
  description: string
  max_concurrent_tasks: number
  models: string[]
  agents: string[]
  capabilities: string[]
  is_active: boolean
  created_at: string
}

export interface Agent {
  id: string
  name: string
  description: string
  category: string
  model_provider: string
  model_name: string
  tools: string[]
  capabilities: string[]
  is_active: boolean
  created_at: string
}

export interface ModelProvider {
  id: string
  name: string
  base_url: string
  models: any[]
  rate_limit: number
  is_active: boolean
  created_at: string
}

export interface Task {
  id: string
  title: string
  description: string
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled'
  priority: number
  input_data: any
  output_data: any
  error_message: string
  created_at: string
  updated_at: string
  completed_at: string
}

export interface SystemStatus {
  cpu_usage: number
  memory_usage: number
  disk_usage: number
  active_tasks: number
  active_agents: number
  active_brains: number
  uptime: number
}
