<template>
  <div class="brains-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>大脑管理</span>
          <el-button type="primary" @click="showAddDialog = true">
            <el-icon><Plus /></el-icon>
            添加大脑
          </el-button>
        </div>
      </template>
      
      <el-table :data="brains" stripe>
        <el-table-column prop="name" label="名称" />
        <el-table-column prop="brain_type" label="类型">
          <template #default="{ row }">
            <el-tag>{{ row.brain_type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" />
        <el-table-column prop="max_concurrent_tasks" label="最大并发" width="100" />
        <el-table-column prop="is_active" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'">
              {{ row.is_active ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button size="small" @click="editBrain(row)">编辑</el-button>
            <el-button size="small" :type="row.is_active ? 'danger' : 'success'" @click="toggleBrain(row)">
              {{ row.is_active ? '禁用' : '启用' }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 添加/编辑对话框 -->
    <el-dialog v-model="showAddDialog" :title="editingBrain ? '编辑大脑' : '添加大脑'" width="500px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="名称">
          <el-input v-model="form.name" placeholder="请输入大脑名称" />
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="form.brain_type" placeholder="请选择类型">
            <el-option label="主大脑" value="master" />
            <el-option label="营销大脑" value="marketing" />
            <el-option label="开发大脑" value="development" />
            <el-option label="设计大脑" value="design" />
            <el-option label="销售大脑" value="sales" />
            <el-option label="分析大脑" value="analytics" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入描述" />
        </el-form-item>
        <el-form-item label="最大并发">
          <el-input-number v-model="form.max_concurrent_tasks" :min="1" :max="20" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="saveBrain">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { brainApi } from '@/api'
import type { Brain } from '@/types'
import { ElMessage } from 'element-plus'

const brains = ref<Brain[]>([])
const showAddDialog = ref(false)
const editingBrain = ref<Brain | null>(null)

const form = ref({
  name: '',
  brain_type: '',
  description: '',
  max_concurrent_tasks: 5
})

const editBrain = (brain: Brain) => {
  editingBrain.value = brain
  form.value = {
    name: brain.name,
    brain_type: brain.brain_type,
    description: brain.description,
    max_concurrent_tasks: brain.max_concurrent_tasks
  }
  showAddDialog.value = true
}

const toggleBrain = async (brain: Brain) => {
  try {
    await brainApi.update(brain.id, { ...brain, is_active: !brain.is_active })
    ElMessage.success(`大脑已${brain.is_active ? '禁用' : '启用'}`)
    await loadBrains()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const saveBrain = async () => {
  try {
    if (editingBrain.value) {
      await brainApi.update(editingBrain.value.id, form.value)
      ElMessage.success('更新成功')
    } else {
      await brainApi.create(form.value)
      ElMessage.success('创建成功')
    }
    showAddDialog.value = false
    editingBrain.value = null
    form.value = { name: '', brain_type: '', description: '', max_concurrent_tasks: 5 }
    await loadBrains()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const loadBrains = async () => {
  try {
    brains.value = await brainApi.list() as Brain[]
  } catch (error) {
    console.error('Failed to load brains:', error)
  }
}

onMounted(loadBrains)
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
