<template>
  <div class="tasks-container">
    <div class="page-header">
      <h2>任务管理</h2>
      <el-button type="primary" @click="showAddDialog = true">
        <el-icon><Plus /></el-icon>
        创建任务
      </el-button>
    </div>

    <!-- 任务筛选 -->
    <div class="task-filters">
      <el-radio-group v-model="statusFilter" @change="fetchTasks">
        <el-radio-button label="">全部</el-radio-button>
        <el-radio-button label="pending">待执行</el-radio-button>
        <el-radio-button label="running">执行中</el-radio-button>
        <el-radio-button label="completed">已完成</el-radio-button>
        <el-radio-button label="failed">失败</el-radio-button>
      </el-radio-group>
    </div>

    <!-- 任务列表 -->
    <el-table :data="taskStore.tasks" stripe v-loading="taskStore.loading">
      <el-table-column prop="title" label="任务标题" />
      <el-table-column prop="status" label="状态">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">
            {{ getStatusLabel(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="priority" label="优先级" width="80" />
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150">
        <template #default="{ row }">
          <el-button size="small" @click="viewTask(row)">查看</el-button>
          <el-button 
            v-if="row.status === 'pending' || row.status === 'running'"
            size="small" 
            type="danger"
            @click="taskStore.cancelTask(row.id)"
          >
            取消
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 创建任务对话框 -->
    <el-dialog v-model="showAddDialog" title="创建任务" width="500px">
      <el-form :model="taskForm" label-width="100px">
        <el-form-item label="任务标题">
          <el-input v-model="taskForm.title" placeholder="请输入任务标题" />
        </el-form-item>
        <el-form-item label="任务描述">
          <el-input v-model="taskForm.description" type="textarea" placeholder="请输入任务描述" />
        </el-form-item>
        <el-form-item label="优先级">
          <el-input-number v-model="taskForm.priority" :min="0" :max="10" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="addTask">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useTaskStore } from '@/stores'
import { Plus } from '@element-plus/icons-vue'

const taskStore = useTaskStore()
const statusFilter = ref('')
const showAddDialog = ref(false)
const taskForm = ref({
  title: '',
  description: '',
  priority: 0
})

onMounted(() => {
  fetchTasks()
})

function fetchTasks() {
  taskStore.fetchTasks(statusFilter.value || undefined)
}

function getStatusType(status: string) {
  const types: Record<string, string> = {
    pending: 'info',
    running: 'warning',
    completed: 'success',
    failed: 'danger',
    cancelled: 'info'
  }
  return types[status] || 'info'
}

function getStatusLabel(status: string) {
  const labels: Record<string, string> = {
    pending: '待执行',
    running: '执行中',
    completed: '已完成',
    failed: '失败',
    cancelled: '已取消'
  }
  return labels[status] || status
}

function formatDate(date: string) {
  if (!date) return '-'
  return new Date(date).toLocaleString('zh-CN')
}

function viewTask(task: any) {
  // TODO: 实现查看详情功能
  console.log('查看任务:', task)
}

async function addTask() {
  await taskStore.createTask(taskForm.value)
  showAddDialog.value = false
  taskForm.value = { title: '', description: '', priority: 0 }
}
</script>

<style scoped>
.tasks-container {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.task-filters {
  margin-bottom: 16px;
}
</style>
