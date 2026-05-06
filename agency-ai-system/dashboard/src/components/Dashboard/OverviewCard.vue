<template>
  <div class="overview-card">
    <el-card>
      <div class="card-body">
        <div class="card-icon" :style="{ backgroundColor: color }">
          <el-icon :size="28"><component :is="icon" /></el-icon>
        </div>
        <div class="card-info">
          <div class="card-value">{{ value }}</div>
          <div class="card-label">{{ label }}</div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  icon: any
  value: string | number
  label: string
  color?: string
}>()
</script>

<style scoped>
.overview-card {
  margin-bottom: 16px;
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
</style>
