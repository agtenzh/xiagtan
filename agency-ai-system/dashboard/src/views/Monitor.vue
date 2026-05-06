<template>
  <div class="monitor-container">
    <!-- 系统状态卡片 -->
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card>
          <template #header>系统状态</template>
          <div class="status-item">
            <span>CPU使用率</span>
            <el-progress :percentage="systemStatus.cpu_usage" :color="getStatusColor(systemStatus.cpu_usage)" />
          </div>
          <div class="status-item">
            <span>内存使用率</span>
            <el-progress :percentage="systemStatus.memory_usage" :color="getStatusColor(systemStatus.memory_usage)" />
          </div>
          <div class="status-item">
            <span>磁盘使用率</span>
            <el-progress :percentage="systemStatus.disk_usage" :color="getStatusColor(systemStatus.disk_usage)" />
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="18">
        <el-card>
          <template #header>任务执行趋势</template>
          <div ref="taskChart" style="height: 300px;"></div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 代理负载分布 -->
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="12">
        <el-card>
          <template #header>代理负载分布</template>
          <div ref="agentChart" style="height: 300px;"></div>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card>
          <template #header>最近日志</template>
          <div class="log-list">
            <div v-for="(log, index) in recentLogs" :key="index" class="log-item">
              <el-tag :type="getLogLevelType(log.level)" size="small">{{ log.level }}</el-tag>
              <span class="log-time">{{ log.time }}</span>
              <span class="log-message">{{ log.message }}</span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { systemApi } from '@/api'
import type { SystemStatus } from '@/types'

const systemStatus = ref<SystemStatus>({
  cpu_usage: 0,
  memory_usage: 0,
  disk_usage: 0,
  active_tasks: 0,
  active_agents: 0,
  active_brains: 0,
  uptime: 0
})

const recentLogs = ref([
  { level: 'INFO', time: '14:30:25', message: '系统启动完成' },
  { level: 'INFO', time: '14:30:26', message: '大脑初始化完成' },
  { level: 'INFO', time: '14:30:27', message: '代理池初始化完成' },
  { level: 'WARNING', time: '14:31:00', message: 'CPU使用率超过80%' },
  { level: 'ERROR', time: '14:32:00', message: '代理执行任务失败' }
])

const getStatusColor = (percentage: number) => {
  if (percentage > 90) return '#F56C6C'
  if (percentage > 70) return '#E6A23C'
  return '#67C23A'
}

const getLogLevelType = (level: string) => {
  const types: Record<string, string> = {
    INFO: 'info',
    WARNING: 'warning',
    ERROR: 'danger',
    DEBUG: ''
  }
  return types[level] || ''
}

onMounted(async () => {
  try {
    const status = await systemApi.getStatus()
    systemStatus.value = status as SystemStatus
  } catch (error) {
    console.error('Failed to load system status:', error)
  }
})
</script>

<style scoped>
.status-item {
  margin-bottom: 16px;
}

.status-item span {
  display: block;
  margin-bottom: 8px;
  color: #606266;
}

.log-list {
  max-height: 300px;
  overflow-y: auto;
}

.log-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 0;
  border-bottom: 1px solid #ebeef5;
}

.log-time {
  color: #909399;
  font-size: 12px;
}

.log-message {
  flex: 1;
  font-size: 14px;
}
</style>
