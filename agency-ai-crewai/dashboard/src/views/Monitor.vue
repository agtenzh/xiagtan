<template>
  <div class="monitor-container">
    <div class="page-header">
      <h2>系统监控</h2>
      <el-button @click="refreshData">
        <el-icon><Refresh /></el-icon>
        刷新
      </el-button>
    </div>

    <div class="overview-cards">
      <el-card class="overview-card">
        <div class="card-body">
          <div class="card-icon" style="background-color: #3b82f6;">
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
          <div class="card-icon" style="background-color: #10b981;">
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
          <div class="card-icon" style="background-color: #f59e0b;">
            <el-icon><Cpu /></el-icon>
          </div>
          <div class="card-info">
            <div class="card-value">{{ systemStatus.active_brains || 0 }}</div>
            <div class="card-label">活跃大脑</div>
          </div>
        </div>
      </el-card>

      <el-card class="overview-card">
        <div class="card-body">
          <div class="card-icon" style="background-color: #8b5cf6;">
            <el-icon><User /></el-icon>
          </div>
          <div class="card-info">
            <div class="card-value">{{ systemStatus.active_agents || 0 }}</div>
            <div class="card-label">活跃代理</div>
          </div>
        </div>
      </el-card>
    </div>

    <el-card class="crew-status">
      <template #header>
        <span>Crew状态</span>
      </template>
      <div v-if="systemStatus.crew_status?.sub_crews" class="crews-grid">
        <el-card v-for="(crew, name) in systemStatus.crew_status.sub_crews" :key="name" class="crew-card">
          <h3>{{ crew.name }}</h3>
          <p>{{ crew.description }}</p>
          <div class="crew-stats">
            <el-tag size="small">代理: {{ crew.agents }}</el-tag>
            <el-tag size="small" type="success">完成: {{ crew.completed_tasks }}</el-tag>
          </div>
        </el-card>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { Refresh, Cpu, Coin, User } from '@element-plus/icons-vue'
import api from '@/api'

const systemStatus = ref<any>({})
let refreshTimer: any = null

onMounted(() => {
  refreshData()
  refreshTimer = setInterval(refreshData, 10000)
})

onUnmounted(() => {
  if (refreshTimer) clearInterval(refreshTimer)
})

async function refreshData() {
  try {
    const response = await api.get('/system/status')
    systemStatus.value = response.data
  } catch (error) {
    console.error('获取系统状态失败:', error)
  }
}
</script>

<style scoped>
.monitor-container {
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
  border-radius: 12px;
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
  color: #1e293b;
}

.card-label {
  font-size: 14px;
  color: #64748b;
}

.crews-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 16px;
}

.crew-card h3 {
  margin: 0 0 8px 0;
  color: #1e293b;
}

.crew-card p {
  margin: 0 0 12px 0;
  color: #64748b;
  font-size: 14px;
}

.crew-stats {
  display: flex;
  gap: 8px;
}
</style>
