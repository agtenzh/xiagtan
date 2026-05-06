<template>
  <div class="node-detail">
    <el-descriptions :column="1" border>
      <el-descriptions-item label="ID">{{ node.id }}</el-descriptions-item>
      <el-descriptions-item label="名称">{{ node.label }}</el-descriptions-item>
      <el-descriptions-item label="类型">
        <el-tag :type="getTypeTag(node.type)">{{ node.type }}</el-tag>
      </el-descriptions-item>
      <el-descriptions-item label="状态">
        <el-tag :type="getStatusTag(node.status)">{{ node.status }}</el-tag>
      </el-descriptions-item>
    </el-descriptions>
    
    <div class="actions" v-if="showActions">
      <el-button size="small" @click="$emit('edit', node)">编辑</el-button>
      <el-button size="small" :type="node.status === 'online' ? 'danger' : 'success'" 
                 @click="$emit('toggle', node)">
        {{ node.status === 'online' ? '下线' : '上线' }}
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Node {
  id: string
  label: string
  type: string
  status: string
}

defineProps<{
  node: Node
  showActions?: boolean
}>()

defineEmits<{
  (e: 'edit', node: Node): void
  (e: 'toggle', node: Node): void
}>()

const getTypeTag = (type: string) => {
  const tags: Record<string, string> = {
    brain: 'primary',
    agent: 'success',
    model: 'warning'
  }
  return tags[type] || 'info'
}

const getStatusTag = (status: string) => {
  const tags: Record<string, string> = {
    online: 'success',
    offline: 'danger',
    busy: 'warning'
  }
  return tags[status] || 'info'
}
</script>

<style scoped>
.node-detail {
  padding: 16px;
}

.actions {
  margin-top: 16px;
  display: flex;
  gap: 8px;
}
</style>
