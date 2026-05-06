<template>
  <div class="dashboard-container">
    <div class="page-header">
      <h2>系统监控</h2>
      <el-button @click="refreshData">
        <el-icon><Refresh /></el-icon>
        刷新
      </el-button>
    </div>

    <!-- 概览卡片 -->
    <div class="overview-cards">
      <el-card class="overview-card">
        <div class="card-body">
          <div class="card-icon" style="background-color: #409eff;">
            <el-icon><Cpu /></el-icon>
          </div>
          <div class="card-info">
            <div class="card-value">{{ systemStatus.cpu_usage || 0 }}%</div>
            <div class="card-label">CPU使用率</div>
          </div>
        </div>
      </el-card>

      <el-card class="overview-card">
        <div class="card-body">
          <div class="card-icon" style="background-color: #67c23a;">
            <el-icon><Coin /></el-icon>
          </div>
          <div class="card-info">
            <div class="card-value">{{ systemStatus.memory_usage || 0 }}%</div>
            <div class="card-label">内存使用率</div>
          </div>
        </div>
      </el-card>

      <el-card class="overview-card">
        <div class="card-body">
          <div class="card-icon" style="background-color: #e6a23c;">
            <el-icon><List /></el-icon>
          </div>
          <div class="card-info">
            <div class="card-value">{{ progressStatus.summary?.running_tasks || 0 }}</div>
            <div class="card-label">运行中任务</div>
          </div>
        </div>
      </el-card>

      <el-card class="overview-card">
        <div class="card-body">
          <div class="card-icon" style="background-color: #f56c6c;">
            <el-icon><User /></el-icon>
          </div>
          <div class="card-info">
            <div class="card-value">{{ progressStatus.threads?.busy || 0 }}/{{ progressStatus.threads?.total || 0 }}</div>
            <div class="card-label">忙碌线程</div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 状态详情 -->
    <div class="status-details">
      <!-- 健康状态 -->
      <el-card class="detail-card">
        <template #header>
          <span>系统健康状态</span>
        </template>
        <div class="health-status">
          <el-tag :type="getHealthType(healthStatus.status)" size="large">
            {{ getHealthLabel(healthStatus.status) }}
          </el-tag>
          <div class="health-info">
            <p>健康组件: {{ healthStatus.healthy || 0 }}</p>
            <p>异常组件: {{ healthStatus.unhealthy || 0 }}</p>
          </div>
        </div>
      </el-card>

      <!-- 任务统计 -->
      <el-card class="detail-card">
        <template #header>
          <span>任务统计</span>
        </template>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="总任务数">{{ progressStatus.summary?.total_tasks || 0 }}</el-descriptions-item>
          <el-descriptions-item label="已完成">{{ progressStatus.summary?.completed_tasks || 0 }}</el-descriptions-item>
          <el-descriptions-item label="运行中">{{ progressStatus.summary?.running_tasks || 0 }}</el-descriptions-item>
          <el-descriptions-item label="失败">{{ progressStatus.summary?.failed_tasks || 0 }}</el-descriptions-item>
          <el-descriptions-item label="完成率">{{ (progressStatus.summary?.completion_rate || 0).toFixed(1) }}%</el-descriptions-item>
        </el-descriptions>
      </el-card>
    </div>

    <!-- 运行中的任务 -->
    <el-card class="running-tasks" v-if="progressStatus.running_tasks?.length">
      <template #header>
        <span>运行中的任务</span>
      </template>
      <el-table :data="progressStatus.running_tasks" stripe>
        <el-table-column prop="task_name" label="任务名称" />
        <el-table-column prop="thread_id" label="执行线程" />
        <el-table-column prop="progress" label="进度">
          <template #default="{ row }">
            <el-progress :percentage="row.progress" :stroke-width="10" />
          </template>
        </el-table-column>
        <el-table-column label="耗时">
          <template #default="{ row }">
            {{ formatTime(row.elapsed_time) }}
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { Refresh, Cpu, Coin, List, User } from '@element-plus/icons-vue'
import api from '@/api'

const systemStatus = ref<any>({})
const healthStatus = ref<any>({})
const progressStatus = ref<any>({})
let refreshTimer: any = null

onMounted(() => {
  refreshData()
  // 每10秒自动刷新
  refreshTimer = setInterval(refreshData, 10000)
})

onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
})

async function refreshData() {
  try {
    const [system, health, progress] = await Promise.all([
      api.getSystemStatus(),
      api.getHealthCheck(),
      api.getProgressReport()
    ])
    systemStatus.value = system
    healthStatus.value = health
    progressStatus.value = progress
  } catch (error) {
    console.error('获取监控数据失败:', error)
  }
}

function getHealthType(status: string) {
  const types: Record<string, string> = {
    healthy: 'success',
    degraded: 'warning',
    unhealthy: 'danger',
    unknown: 'info'
  }
  return types[status] || 'info'
}

function getHealthLabel(status: string) {
  const labels: Record<string, string> = {
    healthy: '健康',
    degraded: '降级',
    unhealthy: '不健康',
    unknown: '未知'
  }
  return labels[status] || '未知'
}

function formatTime(seconds: number) {
  if (!seconds) return '-'
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}分${secs}秒`
}
</script>

<style scoped>
.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.overview-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.card-body {
  display: flex;
  align-items: center;
}

.card-icon {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
}

.card-icon .el-icon {
  font-size: 28px;
  color: #fff;
}

.card-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}

.card-label {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}

.status-details {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.health-status {
  display: flex;
  align-items: center;
  gap: 16px;
}

.health-info p {
  margin: 4px 0;
  color: #606266;
}

.running-tasks {
  margin-bottom: 24px;
}
</style>
