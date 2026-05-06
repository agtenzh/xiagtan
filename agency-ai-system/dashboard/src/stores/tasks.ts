import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api'

export default defineStore('tasks', () => {
  const tasks = ref<any[]>([])
  const loading = ref(false)

  async function fetchTasks(status?: string) {
    loading.value = true
    try {
      tasks.value = await api.getTasks(status)
    } catch (error) {
      console.error('获取任务列表失败:', error)
    } finally {
      loading.value = false
    }
  }

  async function createTask(task: any) {
    try {
      await api.createTask(task)
      await fetchTasks()
    } catch (error) {
      console.error('创建任务失败:', error)
    }
  }

  async function cancelTask(id: string) {
    try {
      await api.cancelTask(id)
      await fetchTasks()
    } catch (error) {
      console.error('取消任务失败:', error)
    }
  }

  return { tasks, loading, fetchTasks, createTask, cancelTask }
})
