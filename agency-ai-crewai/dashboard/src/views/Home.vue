<template>
  <div class="home-container">
    <h1>AI多代理系统 - CrewAI</h1>
    <p class="subtitle">基于CrewAI框架的智能代理协作平台</p>

    <!-- 概览卡片 -->
    <div class="overview-cards">
      <el-card class="overview-card">
        <div class="card-body">
          <div class="card-icon" style="background-color: #3b82f6;">
            <el-icon><Cpu /></el-icon>
          </div>
          <div class="card-info">
            <div class="card-value">{{ brains.length }}</div>
            <div class="card-label">大脑数量</div>
          </div>
        </div>
      </el-card>

      <el-card class="overview-card">
        <div class="card-body">
          <div class="card-icon" style="background-color: #10b981;">
            <el-icon><User /></el-icon>
          </div>
          <div class="card-info">
            <div class="card-value">{{ agents.length }}</div>
            <div class="card-label">代理数量</div>
          </div>
        </div>
      </el-card>

      <el-card class="overview-card">
        <div class="card-body">
          <div class="card-icon" style="background-color: #f59e0b;">
            <el-icon><List /></el-icon>
          </div>
          <div class="card-info">
            <div class="card-value">{{ tasks.length }}</div>
            <div class="card-label">任务数量</div>
          </div>
        </div>
      </el-card>

      <el-card class="overview-card">
        <div class="card-body">
          <div class="card-icon" style="background-color: #8b5cf6;">
            <el-icon><DataLine /></el-icon>
          </div>
          <div class="card-info">
            <div class="card-value">{{ systemStatus.cpu_usage || 0 }}%</div>
            <div class="card-label">CPU使用率</div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 快速操作 -->
    <el-card class="quick-actions">
      <template #header>
        <span>快速操作</span>
      </template>
      <div class="actions-grid">
        <el-button type="primary" @click="$router.push('/brains')">
          <el-icon><Cpu /></el-icon>
          管理大脑
        </el-button>
        <el-button type="success" @click="$router.push('/agents')">
          <el-icon><User /></el-icon>
          管理代理
        </el-button>
        <el-button type="warning" @click="$router.push('/tasks')">
          <el-icon><List /></el-icon>
          创建任务
        </el-button>
        <el-button type="info" @click="$router.push('/monitor')">
          <el-icon><DataLine /></el-icon>
          系统监控
        </el-button>
      </div>
    </el-card>

    <!-- 大脑列表 -->
    <el-card class="brains-list">
      <template #header>
        <div class="card-header">
          <span>大脑列表</span>
          <el-tag type="success">{{ brains.length }} 个</el-tag>
        </div>
      </template>
      <div class="brains-grid">
        <el-card v-for="brain in brains" :key="brain.id" class="brain-card" shadow="hover">
          <div class="brain-info">
            <div class="brain-icon" :style="{ backgroundColor: getBrainColor(brain.brain_type) }">
              <el-icon><Cpu /></el-icon>
            </div>
            <div class="brain-details">
              <h3>{{ brain.name }}</h3>
              <p>{{ brain.description }}</p>
              <div class="brain-meta">
                <el-tag size="small">{{ brain.brain_type }}</el-tag>
                <el-tag size="small" type="success">{{ brain.agents?.length || 0 }} 个代理</el-tag>
              </div>
            </div>
          </div>
        </el-card>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Cpu, User, List, DataLine } from '@element-plus/icons-vue'
import api from '@/api'

const brains = ref<any[]>([])
const agents = ref<any[]>([])
const tasks = ref<any[]>([])
const systemStatus = ref<any>({})

onMounted(() => {
  fetchData()
})

async function fetchData() {
  try {
    const [brainsRes, agentsRes, tasksRes, statusRes] = await Promise.all([
      api.get('/brains'),
      api.get('/agents'),
      api.get('/tasks'),
      api.get('/system/status')
    ])
    brains.value = brainsRes.data
    agents.value = agentsRes.data
    tasks.value = tasksRes.data
    systemStatus.value = statusRes.data
  } catch (error) {
    console.error('获取数据失败:', error)
  }
}

function getBrainColor(type: string) {
  const colors: Record<string, string> = {
    master: '#3b82f6',
    marketing: '#10b981',
    engineering: '#f59e0b',
    design: '#ec4899',
    sales: '#8b5cf6'
  }
  return colors[type] || '#6b7280'
}
</script>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  margin-bottom: 8px;
  color: #1e293b;
}

.subtitle {
  color: #64748b;
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
  font-size: 32px;
  font-weight: bold;
  color: #1e293b;
}

.card-label {
  font-size: 14px;
  color: #64748b;
  margin-top: 4px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.brains-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.brain-card {
  cursor: pointer;
  transition: all 0.3s;
}

.brain-card:hover {
  transform: translateY(-2px);
}

.brain-info {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.brain-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.brain-icon .el-icon {
  font-size: 24px;
  color: #fff;
}

.brain-details h3 {
  margin: 0 0 8px 0;
  font-size: 16px;
  color: #1e293b;
}

.brain-details p {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #64748b;
}

.brain-meta {
  display: flex;
  gap: 8px;
}
</style>
