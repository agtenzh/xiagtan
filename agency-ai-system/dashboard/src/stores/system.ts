import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api'

export default defineStore('system', () => {
  const status = ref({
    cpu_usage: 0,
    memory_usage: 0,
    disk_usage: 0,
    active_tasks: 0,
    active_agents: 0,
    active_brains: 0,
    uptime: 0
  })

  const loading = ref(false)

  async function fetchStatus() {
    loading.value = true
    try {
      const data = await api.getSystemStatus()
      status.value = data
    } catch (error) {
      console.error('获取系统状态失败:', error)
    } finally {
      loading.value = false
    }
  }

  return { status, loading, fetchStatus }
})
