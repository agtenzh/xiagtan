<template>
  <div class="logs-container">
    <div class="page-header">
      <h2>日志查看</h2>
      <div class="header-actions">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索日志..."
          style="width: 200px; margin-right: 16px;"
          @keyup.enter="searchLogs"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-button @click="fetchLogs">刷新</el-button>
      </div>
    </div>

    <!-- 日志筛选 -->
    <div class="log-filters">
      <el-select v-model="categoryFilter" placeholder="类别" clearable @change="fetchLogs">
        <el-option label="任务" value="task" />
        <el-option label="代理" value="agent" />
        <el-option label="大脑" value="brain" />
        <el-option label="系统" value="system" />
      </el-select>
      <el-select v-model="levelFilter" placeholder="级别" clearable @change="fetchLogs">
        <el-option label="信息" value="INFO" />
        <el-option label="成功" value="SUCCESS" />
        <el-option label="警告" value="WARNING" />
        <el-option label="错误" value="ERROR" />
      </el-select>
    </div>

    <!-- 日志列表 -->
    <el-table :data="logs" stripe v-loading="loading">
      <el-table-column prop="timestamp" label="时间" width="180">
        <template #default="{ row }">
          {{ formatDate(row.timestamp) }}
        </template>
      </el-table-column>
      <el-table-column prop="level" label="级别" width="100">
        <template #default="{ row }">
          <el-tag :type="getLevelType(row.level)" size="small">
            {{ row.level }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="category" label="类别" width="100" />
      <el-table-column prop="action" label="操作" width="120" />
      <el-table-column prop="message" label="消息" />
      <el-table-column prop="actor" label="执行者" width="120" />
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/api'
import { Search } from '@element-plus/icons-vue'

const logs = ref<any[]>([])
const loading = ref(false)
const searchKeyword = ref('')
const categoryFilter = ref('')
const levelFilter = ref('')

onMounted(() => {
  fetchLogs()
})

async function fetchLogs() {
  loading.value = true
  try {
    const params: any = { limit: 100 }
    if (categoryFilter.value) params.category = categoryFilter.value
    if (levelFilter.value) params.level = levelFilter.value
    logs.value = await api.getLogs(params)
  } catch (error) {
    console.error('获取日志失败:', error)
  } finally {
    loading.value = false
  }
}

async function searchLogs() {
  if (!searchKeyword.value) {
    fetchLogs()
    return
  }
  loading.value = true
  try {
    logs.value = await api.searchLogs(searchKeyword.value)
  } catch (error) {
    console.error('搜索日志失败:', error)
  } finally {
    loading.value = false
  }
}

function formatDate(date: string) {
  if (!date) return '-'
  return new Date(date).toLocaleString('zh-CN')
}

function getLevelType(level: string) {
  const types: Record<string, string> = {
    INFO: 'info',
    SUCCESS: 'success',
    WARNING: 'warning',
    ERROR: 'danger'
  }
  return types[level] || 'info'
}
</script>

<style scoped>
.logs-container {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.header-actions {
  display: flex;
  align-items: center;
}

.log-filters {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}
</style>
