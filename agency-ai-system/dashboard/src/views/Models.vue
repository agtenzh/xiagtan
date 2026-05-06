<template>
  <div class="models-container">
    <div class="page-header">
      <h2>模型配置</h2>
      <div class="header-actions">
        <el-button type="success" @click="fetchModelsFromProviders">
          <el-icon><Refresh /></el-icon>
          自动获取模型列表
        </el-button>
        <el-button type="primary" @click="showAddDialog = true">
          <el-icon><Plus /></el-icon>
          添加模型
        </el-button>
      </div>
    </div>

    <!-- 主流模型快捷配置 -->
    <el-card class="preset-models">
      <template #header>
        <div class="card-header">
          <span>主流模型快捷配置</span>
          <el-tag type="info">点击添加</el-tag>
        </div>
      </template>
      <div class="preset-grid">
        <div v-for="preset in presetModels" :key="preset.name" class="preset-item" @click="addPresetModel(preset)">
          <div class="preset-icon" :style="{ backgroundColor: preset.color }">
            <span>{{ preset.icon }}</span>
          </div>
          <div class="preset-info">
            <h4>{{ preset.name }}</h4>
            <p>{{ preset.description }}</p>
            <div class="preset-models-list">
              <el-tag v-for="model in preset.models" :key="model" size="small" type="info">
                {{ model }}
              </el-tag>
            </div>
          </div>
          <el-button size="small" type="primary">添加</el-button>
        </div>
      </div>
    </el-card>

    <!-- 已配置模型列表 -->
    <el-card class="configured-models">
      <template #header>
        <div class="card-header">
          <span>已配置模型</span>
          <el-tag type="success">{{ models.length }} 个</el-tag>
        </div>
      </template>

      <el-table :data="models" stripe v-loading="loading">
        <el-table-column prop="name" label="模型名称" width="180" />
        <el-table-column prop="base_url" label="API端点" />
        <el-table-column label="包含模型">
          <template #default="{ row }">
            <div class="models-tags">
              <el-tag v-for="model in (row.models || []).slice(0, 3)" :key="model.name" size="small" style="margin-right: 4px;">
                {{ model.name }}
              </el-tag>
              <el-tag v-if="(row.models || []).length > 3" size="small" type="info">
                +{{ (row.models || []).length - 3 }}
              </el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="rate_limit" label="速率限制" width="100">
          <template #default="{ row }">
            {{ row.rate_limit || '-' }}/min
          </template>
        </el-table-column>
        <el-table-column prop="is_active" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'" size="small">
              {{ row.is_active ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button size="small" @click="editModel(row)">编辑</el-button>
            <el-button size="small" @click="testModel(row)">测试</el-button>
            <el-button size="small" :type="row.is_active ? 'danger' : 'success'" @click="toggleModel(row)">
              {{ row.is_active ? '禁用' : '启用' }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 自动获取模型对话框 -->
    <el-dialog v-model="showFetchDialog" title="自动获取模型列表" width="600px">
      <div class="fetch-content">
        <p>选择要获取模型列表的提供商：</p>
        <div class="provider-list">
          <el-checkbox v-for="provider in availableProviders" :key="provider.id" v-model="provider.selected">
            <div class="provider-item">
              <span class="provider-icon">{{ provider.icon }}</span>
              <span>{{ provider.name }}</span>
            </div>
          </el-checkbox>
        </div>
        
        <div v-if="fetchingModels" class="fetching-status">
          <el-icon class="is-loading"><Loading /></el-icon>
          <span>正在获取模型列表...</span>
        </div>
        
        <div v-if="fetchedModels.length > 0" class="fetched-models">
          <h4>获取到的模型：</h4>
          <div class="model-list">
            <el-tag v-for="model in fetchedModels" :key="model" type="success" style="margin: 4px;">
              {{ model }}
            </el-tag>
          </div>
        </div>
      </div>
      <template #footer>
        <el-button @click="showFetchDialog = false">取消</el-button>
        <el-button type="primary" @click="saveFetchedModels" :disabled="fetchedModels.length === 0">
          保存模型列表
        </el-button>
      </template>
    </el-dialog>

    <!-- 添加/编辑模型对话框 -->
    <el-dialog v-model="showAddDialog" :title="isEdit ? '编辑模型' : '添加模型'" width="500px" top="5vh">
      <el-scrollbar max-height="60vh">
        <el-form :model="modelForm" label-width="100px" label-position="left">
          <el-form-item label="模型名称">
            <el-input v-model="modelForm.name" placeholder="例如：OpenAI GPT-4" size="small" />
          </el-form-item>
          <el-form-item label="提供商">
            <el-select v-model="modelForm.provider" placeholder="选择提供商" @change="onProviderChange" size="small" style="width: 100%;">
              <el-option label="OpenAI" value="openai" />
              <el-option label="Anthropic" value="anthropic" />
              <el-option label="Google" value="google" />
              <el-option label="本地模型" value="local" />
              <el-option label="DeepSeek" value="deepseek" />
              <el-option label="通义千问" value="qwen" />
              <el-option label="自定义" value="custom" />
            </el-select>
          </el-form-item>
          <el-form-item label="API端点">
            <el-input v-model="modelForm.base_url" placeholder="https://api.openai.com/v1" size="small" />
          </el-form-item>
          <el-form-item label="API密钥">
            <el-input v-model="modelForm.api_key" type="password" show-password placeholder="sk-..." size="small" />
          </el-form-item>
          <el-form-item label="包含模型">
            <div class="models-input-compact">
              <div v-for="(model, index) in modelForm.models" :key="index" class="model-item-compact">
                <el-input v-model="model.name" placeholder="模型名称" size="small" style="flex: 2;" />
                <el-input-number v-model="model.max_tokens" placeholder="Token" size="small" style="flex: 1;" controls-position="right" />
                <el-button type="danger" size="small" @click="removeModel(index)" link>
                  <el-icon><Delete /></el-icon>
                </el-button>
              </div>
              <el-button type="primary" size="small" @click="addModel" link>
                <el-icon><Plus /></el-icon>
                添加模型
              </el-button>
            </div>
          </el-form-item>
          <el-form-item label="速率限制">
            <el-input-number v-model="modelForm.rate_limit" :min="1" :max="1000" size="small" style="width: 120px;" />
            <span style="margin-left: 8px; color: #909399; font-size: 12px;">请求/分钟</span>
          </el-form-item>
          <el-form-item label="启用">
            <el-switch v-model="modelForm.is_active" />
          </el-form-item>
        </el-form>
      </el-scrollbar>
      <template #footer>
        <el-button @click="showAddDialog = false" size="small">取消</el-button>
        <el-button type="primary" @click="saveModel" size="small">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Refresh, Loading } from '@element-plus/icons-vue'
import api from '@/api'

const models = ref<any[]>([])
const loading = ref(false)
const showAddDialog = ref(false)
const showFetchDialog = ref(false)
const isEdit = ref(false)
const editingId = ref('')
const fetchingModels = ref(false)
const fetchedModels = ref<string[]>([])

// 预设模型配置
const presetModels = ref([
  {
    id: 'openai',
    name: 'OpenAI',
    icon: '🤖',
    color: '#10a37f',
    description: 'GPT-4、GPT-3.5等模型',
    models: ['gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo'],
    base_url: 'https://api.openai.com/v1',
    provider: 'openai'
  },
  {
    id: 'anthropic',
    name: 'Anthropic',
    icon: '🧠',
    color: '#d4a574',
    description: 'Claude 3系列模型',
    models: ['claude-3-opus', 'claude-3-sonnet', 'claude-3-haiku'],
    base_url: 'https://api.anthropic.com/v1',
    provider: 'anthropic'
  },
  {
    id: 'google',
    name: 'Google AI',
    icon: '🔍',
    color: '#4285f4',
    description: 'Gemini系列模型',
    models: ['gemini-pro', 'gemini-pro-vision', 'gemini-ultra'],
    base_url: 'https://generativelanguage.googleapis.com/v1',
    provider: 'google'
  },
  {
    id: 'ollama',
    name: 'Ollama (本地)',
    icon: '🦙',
    color: '#000000',
    description: '本地运行的开源模型',
    models: ['llama3', 'mistral', 'codellama', 'qwen2'],
    base_url: 'http://localhost:11434/v1',
    provider: 'local'
  },
  {
    id: 'deepseek',
    name: 'DeepSeek',
    icon: '🔮',
    color: '#0066ff',
    description: 'DeepSeek系列模型',
    models: ['deepseek-chat', 'deepseek-coder'],
    base_url: 'https://api.deepseek.com/v1',
    provider: 'deepseek'
  },
  {
    id: 'qwen',
    name: '通义千问',
    icon: '☁️',
    color: '#ff6a00',
    description: '阿里云通义千问模型',
    models: ['qwen-turbo', 'qwen-plus', 'qwen-max'],
    base_url: 'https://dashscope.aliyuncs.com/api/v1',
    provider: 'qwen'
  }
])

// 可用提供商（用于自动获取）
const availableProviders = ref([
  { id: 'openai', name: 'OpenAI', icon: '🤖', selected: true },
  { id: 'anthropic', name: 'Anthropic', icon: '🧠', selected: true },
  { id: 'google', name: 'Google AI', icon: '🔍', selected: false },
  { id: 'ollama', name: 'Ollama (本地)', icon: '🦙', selected: false }
])

// 模型表单
const modelForm = ref({
  name: '',
  provider: '',
  base_url: '',
  api_key: '',
  models: [{ name: '', max_tokens: 4096, cost_per_1k_tokens: 0 }],
  rate_limit: 60,
  is_active: true
})

// 提供商默认配置
const providerDefaults: Record<string, any> = {
  openai: {
    base_url: 'https://api.openai.com/v1',
    models: [
      { name: 'gpt-4', max_tokens: 8192, cost_per_1k_tokens: 0.03 },
      { name: 'gpt-4-turbo', max_tokens: 128000, cost_per_1k_tokens: 0.01 },
      { name: 'gpt-3.5-turbo', max_tokens: 4096, cost_per_1k_tokens: 0.002 }
    ]
  },
  anthropic: {
    base_url: 'https://api.anthropic.com/v1',
    models: [
      { name: 'claude-3-opus', max_tokens: 4096, cost_per_1k_tokens: 0.015 },
      { name: 'claude-3-sonnet', max_tokens: 4096, cost_per_1k_tokens: 0.003 },
      { name: 'claude-3-haiku', max_tokens: 4096, cost_per_1k_tokens: 0.00025 }
    ]
  },
  google: {
    base_url: 'https://generativelanguage.googleapis.com/v1',
    models: [
      { name: 'gemini-pro', max_tokens: 8192, cost_per_1k_tokens: 0.00025 },
      { name: 'gemini-pro-vision', max_tokens: 4096, cost_per_1k_tokens: 0.00025 }
    ]
  },
  local: {
    base_url: 'http://localhost:11434/v1',
    models: [
      { name: 'llama3', max_tokens: 4096, cost_per_1k_tokens: 0 },
      { name: 'mistral', max_tokens: 4096, cost_per_1k_tokens: 0 },
      { name: 'codellama', max_tokens: 4096, cost_per_1k_tokens: 0 }
    ]
  },
  deepseek: {
    base_url: 'https://api.deepseek.com/v1',
    models: [
      { name: 'deepseek-chat', max_tokens: 4096, cost_per_1k_tokens: 0.002 },
      { name: 'deepseek-coder', max_tokens: 4096, cost_per_1k_tokens: 0.002 }
    ]
  },
  qwen: {
    base_url: 'https://dashscope.aliyuncs.com/api/v1',
    models: [
      { name: 'qwen-turbo', max_tokens: 4096, cost_per_1k_tokens: 0.002 },
      { name: 'qwen-plus', max_tokens: 4096, cost_per_1k_tokens: 0.004 },
      { name: 'qwen-max', max_tokens: 4096, cost_per_1k_tokens: 0.02 }
    ]
  }
}

onMounted(() => {
  fetchModels()
})

async function fetchModels() {
  loading.value = true
  try {
    models.value = await api.getModels()
  } catch (error) {
    console.error('获取模型列表失败:', error)
  } finally {
    loading.value = false
  }
}

function onProviderChange(provider: string) {
  const defaults = providerDefaults[provider]
  if (defaults) {
    modelForm.value.base_url = defaults.base_url
    modelForm.value.models = [...defaults.models]
  }
}

function addModel() {
  modelForm.value.models.push({ name: '', max_tokens: 4096, cost_per_1k_tokens: 0 })
}

function removeModel(index: number) {
  modelForm.value.models.splice(index, 1)
}

function addPresetModel(preset: any) {
  modelForm.value = {
    name: preset.name,
    provider: preset.provider,
    base_url: preset.base_url,
    api_key: '',
    models: preset.models.map((name: string) => ({
      name,
      max_tokens: 4096,
      cost_per_1k_tokens: 0
    })),
    rate_limit: 60,
    is_active: true
  }
  isEdit.value = false
  showAddDialog.value = true
}

function editModel(model: any) {
  modelForm.value = {
    name: model.name,
    provider: model.provider || '',
    base_url: model.base_url || '',
    api_key: '',
    models: model.models || [],
    rate_limit: model.rate_limit || 60,
    is_active: model.is_active
  }
  editingId.value = model.id
  isEdit.value = true
  showAddDialog.value = true
}

async function saveModel() {
  try {
    if (isEdit.value) {
      await api.updateModel(editingId.value, modelForm.value)
      ElMessage.success('模型配置已更新')
    } else {
      await api.createModel(modelForm.value)
      ElMessage.success('模型配置已添加')
    }
    showAddDialog.value = false
    await fetchModels()
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

async function toggleModel(model: any) {
  try {
    await api.updateModel(model.id, { ...model, is_active: !model.is_active })
    ElMessage.success(`模型已${model.is_active ? '禁用' : '启用'}`)
    await fetchModels()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

async function testModel(model: any) {
  ElMessage.info('测试连接中...')
  // TODO: 实现测试连接功能
  setTimeout(() => {
    ElMessage.success('连接测试成功')
  }, 1000)
}

async function fetchModelsFromProviders() {
  showFetchDialog.value = true
  fetchingModels.value = true
  fetchedModels.value = []

  // 模拟获取模型列表
  setTimeout(() => {
    const selectedProviders = availableProviders.value.filter(p => p.selected)
    const allModels: string[] = []

    selectedProviders.forEach(provider => {
      const preset = presetModels.value.find(p => p.id === provider.id)
      if (preset) {
        allModels.push(...preset.models)
      }
    })

    fetchedModels.value = [...new Set(allModels)]
    fetchingModels.value = false
  }, 1500)
}

async function saveFetchedModels() {
  // 为每个提供商创建模型配置
  const selectedProviders = availableProviders.value.filter(p => p.selected)
  
  for (const provider of selectedProviders) {
    const preset = presetModels.value.find(p => p.id === provider.id)
    if (preset) {
      const existingModel = models.value.find(m => m.name === preset.name)
      if (!existingModel) {
        await api.createModel({
          name: preset.name,
          provider: preset.provider,
          base_url: preset.base_url,
          api_key: '',
          models: preset.models.map(name => ({
            name,
            max_tokens: 4096,
            cost_per_1k_tokens: 0
          })),
          rate_limit: 60,
          is_active: true
        })
      }
    }
  }

  ElMessage.success('模型配置已保存')
  showFetchDialog.value = false
  await fetchModels()
}
</script>

<style scoped>
.models-container {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 预设模型样式 */
.preset-models {
  margin-bottom: 24px;
}

.preset-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 16px;
}

.preset-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.preset-item:hover {
  border-color: #409eff;
  background-color: #f5f7fa;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.preset-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  flex-shrink: 0;
}

.preset-info {
  flex: 1;
}

.preset-info h4 {
  margin: 0 0 4px 0;
  font-size: 16px;
  color: #303133;
}

.preset-info p {
  margin: 0 0 8px 0;
  font-size: 12px;
  color: #909399;
}

.preset-models-list {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

/* 已配置模型样式 */
.configured-models {
  margin-bottom: 24px;
}

.models-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

/* 自动获取对话框样式 */
.fetch-content {
  padding: 16px 0;
}

.provider-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin: 16px 0;
}

.provider-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.provider-icon {
  font-size: 20px;
}

.fetching-status {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 16px 0;
  color: #409eff;
}

.fetched-models {
  margin-top: 16px;
}

.fetched-models h4 {
  margin-bottom: 8px;
}

.model-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

/* 模型输入样式 */
.models-input {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.model-item {
  display: flex;
  gap: 8px;
  align-items: center;
}

/* 紧凑型模型输入 */
.models-input-compact {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
}

.model-item-compact {
  display: flex;
  gap: 8px;
  align-items: center;
  width: 100%;
}

.model-item-compact .el-input {
  flex: 2;
}

.model-item-compact .el-input-number {
  flex: 1;
}

/* 对话框优化 */
:deep(.el-dialog) {
  margin: 0 auto;
}

:deep(.el-dialog__body) {
  padding: 10px 20px;
}

:deep(.el-form-item) {
  margin-bottom: 12px;
}

:deep(.el-form-item__label) {
  font-size: 13px;
}

:deep(.el-input__wrapper),
:deep(.el-select__wrapper) {
  font-size: 13px;
}
</style>
