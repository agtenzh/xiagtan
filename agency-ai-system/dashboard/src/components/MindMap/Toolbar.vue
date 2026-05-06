<template>
  <div class="toolbar">
    <el-button-group>
      <el-button size="small" @click="$emit('zoomIn')">
        <el-icon><ZoomIn /></el-icon>
      </el-button>
      <el-button size="small" @click="$emit('zoomOut')">
        <el-icon><ZoomOut /></el-icon>
      </el-button>
      <el-button size="small" @click="$emit('fitView')">
        <el-icon><FullScreen /></el-icon>
      </el-button>
    </el-button-group>
    
    <el-button-group style="margin-left: 16px;">
      <el-button size="small" @click="$emit('autoLayout')">
        <el-icon><SetUp /></el-icon>
        自动布局
      </el-button>
      <el-button size="small" @click="$emit('refresh')">
        <el-icon><Refresh /></el-icon>
        刷新
      </el-button>
    </el-button-group>
    
    <div class="toolbar-right">
      <el-input
        v-model="searchText"
        size="small"
        placeholder="搜索节点..."
        style="width: 200px;"
        @input="$emit('search', searchText)"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const searchText = ref('')

defineEmits<{
  (e: 'zoomIn'): void
  (e: 'zoomOut'): void
  (e: 'fitView'): void
  (e: 'autoLayout'): void
  (e: 'refresh'): void
  (e: 'search', text: string): void
}>()
</script>

<style scoped>
.toolbar {
  display: flex;
  align-items: center;
  padding: 8px 16px;
  background-color: #fff;
  border-bottom: 1px solid #e6e6e6;
}

.toolbar-right {
  margin-left: auto;
}
</style>
