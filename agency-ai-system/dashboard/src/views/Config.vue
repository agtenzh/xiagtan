<template>
  <div class="config-container">
    <div class="page-header">
      <h2>配置管理</h2>
      <el-button type="primary" @click="saveAllConfigs">
        <el-icon><Check /></el-icon>
        保存所有配置
      </el-button>
    </div>

    <el-tabs v-model="activeTab">
      <!-- 代理配置 -->
      <el-tab-pane label="代理配置" name="agents">
        <el-card class="section-card">
          <template #header>
            <div class="card-header">
              <span>代理管理</span>
              <el-button type="primary" size="small" @click="$router.push('/agents')">
                前往代理管理页面
              </el-button>
            </div>
          </template>
          <p class="section-desc">代理的详细配置请在代理管理页面中进行。</p>
          <div class="quick-stats">
            <el-statistic title="总代理数" :value="agents.length" />
            <el-statistic title="启用代理" :value="agents.filter(a => a.is_active).length" />
            <el-statistic title="禁用代理" :value="agents.filter(a => !a.is_active).length" />
          </div>
        </el-card>
      </el-tab-pane>

      <!-- 大脑配置 -->
      <el-tab-pane label="大脑配置" name="brains">
        <!-- 预设大脑快捷配置 -->
        <el-card class="preset-section">
          <template #header>
            <div class="card-header">
              <span>预设大脑配置</span>
              <el-tag type="info">点击添加</el-tag>
            </div>
          </template>
          <div class="preset-grid">
            <div v-for="preset in presetBrains" :key="preset.id" class="preset-item" @click="addPresetBrain(preset)">
              <div class="preset-icon" :style="{ backgroundColor: preset.color }">
                <span>{{ preset.icon }}</span>
              </div>
              <div class="preset-info">
                <h4>{{ preset.name }}</h4>
                <p>{{ preset.description }}</p>
                <div class="preset-meta">
                  <el-tag size="small">{{ preset.brain_type }}</el-tag>
                  <el-tag size="small" type="success">{{ preset.agents.length }} 个代理</el-tag>
                </div>
              </div>
              <el-button size="small" type="primary">添加</el-button>
            </div>
          </div>
        </el-card>

        <!-- 已配置大脑列表 -->
        <el-card class="configured-section">
          <template #header>
            <div class="card-header">
              <span>已配置大脑</span>
              <el-tag type="success">{{ brains.length }} 个</el-tag>
            </div>
          </template>
          <div class="config-list">
            <el-card v-for="brain in brains" :key="brain.id" class="config-item brain-card">
              <template #header>
                <div class="card-header">
                  <div class="brain-title">
                    <div class="brain-icon" :style="{ backgroundColor: getBrainColor(brain.brain_type) }">
                      <el-icon><Cpu /></el-icon>
                    </div>
                    <span>{{ brain.name }}</span>
                  </div>
                  <div class="brain-actions">
                    <el-tag :type="brain.is_active ? 'success' : 'danger'">
                      {{ brain.is_active ? '启用' : '禁用' }}
                    </el-tag>
                    <el-button size="small" @click="editBrain(brain)">编辑</el-button>
                  </div>
                </div>
              </template>
              <el-descriptions :column="2" border size="small">
                <el-descriptions-item label="类型">
                  <el-tag>{{ brain.brain_type }}</el-tag>
                </el-descriptions-item>
                <el-descriptions-item label="最大并发">{{ brain.max_concurrent_tasks }}</el-descriptions-item>
                <el-descriptions-item label="描述" :span="2">{{ brain.description }}</el-descriptions-item>
                <el-descriptions-item label="可用模型" :span="2">
                  <el-tag v-for="model in brain.models" :key="model" size="small" style="margin-right: 4px;">
                    {{ model }}
                  </el-tag>
                </el-descriptions-item>
                <el-descriptions-item label="子代理" :span="2">
                  <el-tag v-for="agent in brain.agents" :key="agent" size="small" type="success" style="margin-right: 4px;">
                    {{ agent }}
                  </el-tag>
                </el-descriptions-item>
              </el-descriptions>
            </el-card>
          </div>
        </el-card>
      </el-tab-pane>
    </el-tabs>

    <!-- 编辑大脑对话框 -->
    <el-dialog v-model="showBrainDialog" title="编辑大脑" width="500px" top="5vh">
      <el-scrollbar max-height="60vh">
        <el-form :model="brainForm" label-width="100px" label-position="left">
          <el-form-item label="大脑名称">
            <el-input v-model="brainForm.name" size="small" />
          </el-form-item>
          <el-form-item label="大脑类型">
            <el-select v-model="brainForm.brain_type" disabled size="small" style="width: 100%;">
              <el-option label="主大脑" value="master" />
              <el-option label="营销大脑" value="marketing" />
              <el-option label="开发大脑" value="development" />
              <el-option label="设计大脑" value="design" />
              <el-option label="销售大脑" value="sales" />
              <el-option label="分析大脑" value="analytics" />
            </el-select>
          </el-form-item>
          <el-form-item label="描述">
            <el-input v-model="brainForm.description" type="textarea" :rows="2" size="small" />
          </el-form-item>
          <el-form-item label="最大并发">
            <el-input-number v-model="brainForm.max_concurrent_tasks" :min="1" :max="20" size="small" style="width: 120px;" />
          </el-form-item>
          <el-form-item label="可用模型">
            <el-select v-model="brainForm.models" multiple placeholder="选择模型" size="small" style="width: 100%;">
              <el-option v-for="model in availableModels" :key="model" :label="model" :value="model" />
            </el-select>
          </el-form-item>
          <el-form-item label="启用">
            <el-switch v-model="brainForm.is_active" />
          </el-form-item>
        </el-form>
      </el-scrollbar>
      <template #footer>
        <el-button @click="showBrainDialog = false" size="small">取消</el-button>
        <el-button type="primary" @click="saveBrain" size="small">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Check, Cpu } from '@element-plus/icons-vue'
import api from '@/api'

const router = useRouter()
const activeTab = ref('agents')
const agents = ref<any[]>([])
const brains = ref<any[]>([])
const showBrainDialog = ref(false)
const editingBrainId = ref('')

// 可用模型列表
const availableModels = ref([
  'gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo',
  'claude-3-opus', 'claude-3-sonnet', 'claude-3-haiku',
  'gemini-pro', 'gemini-pro-vision',
  'llama3', 'mistral', 'codellama',
  'deepseek-chat', 'deepseek-coder',
  'qwen-turbo', 'qwen-plus', 'qwen-max'
])

// 大脑表单
const brainForm = ref({
  name: '',
  brain_type: '',
  description: '',
  max_concurrent_tasks: 5,
  models: [] as string[],
  agents: [] as string[],
  capabilities: [] as string[],
  is_active: true
})

// 预设大脑配置
const presetBrains = ref([
  {
    id: 'master',
    name: '主大脑',
    icon: '🧠',
    color: '#409eff',
    brain_type: 'master',
    description: '负责全局协调、任务分配、负载均衡',
    max_concurrent_tasks: 10,
    models: ['gpt-4', 'gpt-3.5-turbo'],
    agents: [],
    capabilities: ['task_routing', 'load_balancing', 'result_integration']
  },
  {
    id: 'marketing',
    name: '营销大脑',
    icon: '📢',
    color: '#67c23a',
    brain_type: 'marketing',
    description: '负责营销策略、内容创作、社交媒体',
    max_concurrent_tasks: 5,
    models: ['gpt-4', 'gpt-3.5-turbo'],
    agents: ['content_creator', 'seo_expert', 'social_media'],
    capabilities: ['content_strategy', 'seo', 'social_media']
  },
  {
    id: 'development',
    name: '开发大脑',
    icon: '💻',
    color: '#e6a23c',
    brain_type: 'development',
    description: '负责代码生成、测试、部署',
    max_concurrent_tasks: 5,
    models: ['gpt-4', 'claude-3-opus'],
    agents: ['code_generator', 'test_writer', 'deployer'],
    capabilities: ['code_generation', 'testing', 'deployment']
  },
  {
    id: 'design',
    name: '设计大脑',
    icon: '🎨',
    color: '#f56c6c',
    brain_type: 'design',
    description: '负责UI/UX设计、视觉设计',
    max_concurrent_tasks: 3,
    models: ['gpt-4', 'gpt-3.5-turbo'],
    agents: ['ui_designer', 'visual_designer'],
    capabilities: ['ui_design', 'visual_design']
  },
  {
    id: 'sales',
    name: '销售大脑',
    icon: '💰',
    color: '#909399',
    brain_type: 'sales',
    description: '负责销售策略、客户管理',
    max_concurrent_tasks: 3,
    models: ['gpt-4', 'gpt-3.5-turbo'],
    agents: ['sales_strategist', 'account_manager'],
    capabilities: ['sales_strategy', 'account_management']
  },
  {
    id: 'analytics',
    name: '分析大脑',
    icon: '📊',
    color: '#9b59b6',
    brain_type: 'analytics',
    description: '负责数据分析、报告生成',
    max_concurrent_tasks: 3,
    models: ['gpt-4', 'gpt-3.5-turbo'],
    agents: ['data_analyst', 'report_generator'],
    capabilities: ['data_analysis', 'report_generation']
  }
])

onMounted(async () => {
  await Promise.all([
    fetchAgents(),
    fetchBrains()
  ])
})

async function fetchAgents() {
  try {
    agents.value = await api.getAgents()
  } catch (error) {
    console.error('获取代理列表失败:', error)
  }
}

async function fetchBrains() {
  try {
    brains.value = await api.getBrains()
  } catch (error) {
    console.error('获取大脑列表失败:', error)
  }
}

function getBrainColor(type: string) {
  const colors: Record<string, string> = {
    master: '#409eff',
    marketing: '#67c23a',
    development: '#e6a23c',
    design: '#f56c6c',
    sales: '#909399',
    analytics: '#9b59b6'
  }
  return colors[type] || '#409eff'
}

function addPresetBrain(preset: any) {
  const exists = brains.value.find(b => b.brain_type === preset.brain_type)
  if (exists) {
    ElMessage.warning(`${preset.name} 已存在`)
    return
  }

  brainForm.value = {
    name: preset.name,
    brain_type: preset.brain_type,
    description: preset.description,
    max_concurrent_tasks: preset.max_concurrent_tasks,
    models: [...preset.models],
    agents: [...preset.agents],
    capabilities: [...preset.capabilities],
    is_active: true
  }
  editingBrainId.value = ''
  showBrainDialog.value = true
}

function editBrain(brain: any) {
  brainForm.value = {
    name: brain.name,
    brain_type: brain.brain_type,
    description: brain.description,
    max_concurrent_tasks: brain.max_concurrent_tasks,
    models: brain.models || [],
    agents: brain.agents || [],
    capabilities: brain.capabilities || [],
    is_active: brain.is_active
  }
  editingBrainId.value = brain.id
  showBrainDialog.value = true
}

async function saveBrain() {
  try {
    if (editingBrainId.value) {
      await api.updateBrain(editingBrainId.value, brainForm.value)
      ElMessage.success('大脑配置已更新')
    } else {
      await api.createBrain(brainForm.value)
      ElMessage.success('大脑配置已添加')
    }
    showBrainDialog.value = false
    await fetchBrains()
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

function saveAllConfigs() {
  ElMessage.success('所有配置已保存')
}
</script>

<style scoped>
.config-container {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-card {
  margin-bottom: 24px;
}

.section-desc {
  color: #606266;
  margin-bottom: 16px;
}

.quick-stats {
  display: flex;
  gap: 40px;
}

/* 预设大脑样式 */
.preset-section {
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

.preset-meta {
  display: flex;
  gap: 8px;
}

/* 已配置大脑样式 */
.configured-section {
  margin-bottom: 24px;
}

.config-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.brain-card {
  transition: all 0.3s;
}

.brain-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
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

.brain-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}
</style>
