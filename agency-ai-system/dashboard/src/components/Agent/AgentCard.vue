<template>
  <div class="agent-card">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>{{ agent.name }}</span>
          <el-tag :type="agent.is_active ? 'success' : 'danger'" size="small">
            {{ agent.is_active ? '启用' : '禁用' }}
          </el-tag>
        </div>
      </template>
      
      <div class="card-content">
        <p><strong>类别：</strong>{{ agent.category }}</p>
        <p><strong>模型：</strong>{{ agent.model_provider }}/{{ agent.model_name }}</p>
        <p><strong>描述：</strong>{{ agent.description || '无' }}</p>
        
        <div v-if="agent.capabilities && agent.capabilities.length" class="capabilities">
          <strong>能力：</strong>
          <el-tag v-for="cap in agent.capabilities" :key="cap" size="small" style="margin-right: 4px; margin-top: 4px;">
            {{ cap }}
          </el-tag>
        </div>
      </div>
      
      <div class="card-footer">
        <el-button size="small" @click="$emit('edit', agent)">编辑</el-button>
        <el-button 
          size="small" 
          :type="agent.is_active ? 'danger' : 'success'"
          @click="$emit('toggle', agent)"
        >
          {{ agent.is_active ? '禁用' : '启用' }}
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  agent: any
}>()

defineEmits(['edit', 'toggle'])
</script>

<style scoped>
.agent-card {
  margin-bottom: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-content {
  margin-bottom: 16px;
}

.card-content p {
  margin-bottom: 8px;
  color: #606266;
}

.capabilities {
  margin-top: 12px;
}

.card-footer {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}
</style>
