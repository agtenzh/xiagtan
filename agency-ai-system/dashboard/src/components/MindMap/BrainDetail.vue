<template>
  <div class="brain-detail">
    <el-descriptions :column="1" border>
      <el-descriptions-item label="名称">{{ brain.name }}</el-descriptions-item>
      <el-descriptions-item label="类型">{{ brain.brain_type }}</el-descriptions-item>
      <el-descriptions-item label="描述">{{ brain.description }}</el-descriptions-item>
      <el-descriptions-item label="状态">
        <el-tag :type="brain.is_active ? 'success' : 'danger'">
          {{ brain.is_active ? '在线' : '离线' }}
        </el-tag>
      </el-descriptions-item>
      <el-descriptions-item label="最大并发任务">{{ brain.max_concurrent_tasks }}</el-descriptions-item>
      <el-descriptions-item label="可用模型">
        <el-tag v-for="model in brain.models" :key="model" style="margin-right: 4px;">
          {{ model }}
        </el-tag>
      </el-descriptions-item>
      <el-descriptions-item label="子代理">
        <el-tag v-for="agent in brain.agents" :key="agent" type="success" style="margin-right: 4px;">
          {{ agent }}
        </el-tag>
      </el-descriptions-item>
    </el-descriptions>
    
    <div class="actions">
      <el-button type="primary" @click="$emit('edit', brain)">编辑</el-button>
      <el-button :type="brain.is_active ? 'danger' : 'success'" @click="$emit('toggle', brain)">
        {{ brain.is_active ? '下线' : '上线' }}
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  brain: any
}>()

defineEmits(['edit', 'toggle'])
</script>

<style scoped>
.brain-detail {
  padding: 16px;
}

.actions {
  margin-top: 24px;
  display: flex;
  gap: 16px;
}
</style>
