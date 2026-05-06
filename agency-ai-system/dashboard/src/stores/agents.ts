import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api'

export default defineStore('agents', () => {
  const agents = ref<any[]>([])
  const loading = ref(false)

  async function fetchAgents() {
    loading.value = true
    try {
      agents.value = await api.getAgents()
    } catch (error) {
      console.error('获取代理列表失败:', error)
    } finally {
      loading.value = false
    }
  }

  async function toggleAgent(id: string) {
    try {
      await api.toggleAgent(id)
      await fetchAgents()
    } catch (error) {
      console.error('切换代理状态失败:', error)
    }
  }

  return { agents, loading, fetchAgents, toggleAgent }
})
