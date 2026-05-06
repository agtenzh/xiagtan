<template>
  <div class="brains-container">
    <div class="page-header">
      <h2>大脑管理</h2>
    </div>

    <div class="brains-grid">
      <el-card v-for="brain in brains" :key="brain.id" class="brain-card">
        <template #header>
          <div class="card-header">
            <div class="brain-title">
              <div class="brain-icon" :style="{ backgroundColor: getBrainColor(brain.brain_type) }">
                <el-icon><Cpu /></el-icon>
              </div>
              <span>{{ brain.name }}</span>
            </div>
            <el-tag :type="brain.is_active ? 'success' : 'danger'">
              {{ brain.is_active ? '启用' : '禁用' }}
            </el-tag>
          </div>
        </template>
        <div class="card-content">
          <p><strong>类型：</strong>{{ brain.brain_type }}</p>
          <p><strong>描述：</strong>{{ brain.description || '无' }}</p>
          <p><strong>代理数：</strong>{{ brain.agents?.length || 0 }}</p>
          <p><strong>完成任务：</strong>{{ brain.tasks_completed || 0 }}</p>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Cpu } from '@element-plus/icons-vue'
import api from '@/api'

const brains = ref<any[]>([])

onMounted(async () => {
  try {
    const response = await api.get('/brains')
    brains.value = response.data
  } catch (error) {
    console.error('获取大脑列表失败:', error)
  }
})

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
.brains-container {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 24px;
}

.brains-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brain-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brain-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.brain-icon .el-icon {
  font-size: 18px;
  color: #fff;
}

.card-content p {
  margin-bottom: 8px;
  color: #64748b;
}
</style>
