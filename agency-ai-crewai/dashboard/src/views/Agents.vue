<template>
  <div class="agents-container">
    <div class="page-header">
      <h2>代理管理</h2>
    </div>

    <div class="agents-grid">
      <el-card v-for="agent in agents" :key="agent.id" class="agent-card">
        <template #header>
          <div class="card-header">
            <span>{{ agent.name }}</span>
            <el-tag :type="agent.is_active ? 'success' : 'danger'" size="small">
              {{ agent.is_active ? '启用' : '禁用' }}
            </el-tag>
          </div>
        </template>
        <div class="card-content">
          <p><strong>角色：</strong>{{ agent.role }}</p>
          <p><strong>目标：</strong>{{ agent.goal }}</p>
          <p><strong>类别：</strong>{{ agent.category }}</p>
          <p><strong>模型：</strong>{{ agent.model_provider }}/{{ agent.model_name }}</p>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/api'

const agents = ref<any[]>([])

onMounted(async () => {
  try {
    const response = await api.get('/agents')
    agents.value = response.data
  } catch (error) {
    console.error('获取代理列表失败:', error)
  }
})
</script>

<style scoped>
.agents-container {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 24px;
}

.agents-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-content p {
  margin-bottom: 8px;
  color: #64748b;
}
</style>
