<template>
  <div class="agents-container">
    <div class="page-header">
      <h2>代理管理</h2>
      <el-button type="primary" @click="showAddDialog = true">
        <el-icon><Plus /></el-icon>
        添加代理
      </el-button>
    </div>

    <!-- 代理分类筛选 -->
    <div class="agent-filters">
      <el-radio-group v-model="categoryFilter" @change="fetchAgents">
        <el-radio-button label="">全部</el-radio-button>
        <el-radio-button label="marketing">营销</el-radio-button>
        <el-radio-button label="development">开发</el-radio-button>
        <el-radio-button label="design">设计</el-radio-button>
        <el-radio-button label="sales">销售</el-radio-button>
      </el-radio-group>
    </div>

    <!-- 代理卡片列表 -->
    <div class="agents-grid">
      <el-card v-for="agent in filteredAgents" :key="agent.id" class="agent-card">
        <template #header>
          <div class="card-header">
            <div class="agent-title">
              <div class="agent-icon" :style="{ backgroundColor: getCategoryColor(agent.category) }">
                {{ getCategoryIcon(agent.category) }}
              </div>
              <span>{{ agent.name }}</span>
            </div>
            <el-tag :type="agent.is_active ? 'success' : 'danger'" size="small">
              {{ agent.is_active ? '启用' : '禁用' }}
            </el-tag>
          </div>
        </template>
        <div class="card-content">
          <p><strong>类别：</strong>{{ getCategoryName(agent.category) }}</p>
          <p><strong>模型：</strong>{{ agent.model_provider }}/{{ agent.model_name }}</p>
          <p><strong>描述：</strong>{{ agent.description || '无' }}</p>
          
          <div v-if="agent.capabilities && agent.capabilities.length" class="capabilities">
            <strong>能力：</strong>
            <div class="tags">
              <el-tag v-for="cap in agent.capabilities" :key="cap" size="small" type="info">
                {{ cap }}
              </el-tag>
            </div>
          </div>
          
          <div v-if="agent.tools && agent.tools.length" class="tools">
            <strong>工具：</strong>
            <div class="tags">
              <el-tag v-for="tool in agent.tools" :key="tool" size="small" type="warning">
                {{ tool }}
              </el-tag>
            </div>
          </div>
        </div>
        <div class="card-footer">
          <el-button size="small" @click="editAgent(agent)">
            <el-icon><Edit /></el-icon>
            编辑
          </el-button>
          <el-button size="small" @click="testAgent(agent)">
            <el-icon><VideoPlay /></el-icon>
            测试
          </el-button>
          <el-button 
            size="small" 
            :type="agent.is_active ? 'danger' : 'success'"
            @click="toggleAgent(agent)"
          >
            {{ agent.is_active ? '禁用' : '启用' }}
          </el-button>
        </div>
      </el-card>
    </div>

    <!-- 添加代理对话框 -->
    <el-dialog v-model="showAddDialog" title="添加代理" width="500px" top="5vh">
      <el-scrollbar max-height="60vh">
        <el-form :model="agentForm" label-width="100px" label-position="left">
          <el-form-item label="代理名称">
            <el-input v-model="agentForm.name" placeholder="请输入代理名称" size="small" />
          </el-form-item>
          <el-form-item label="代理类别">
            <el-select v-model="agentForm.category" placeholder="请选择类别" size="small" style="width: 100%;">
              <el-option label="营销" value="marketing" />
              <el-option label="设计" value="design" />
              <el-option label="开发" value="development" />
              <el-option label="销售" value="sales" />
              <el-option label="分析" value="analytics" />
            </el-select>
          </el-form-item>
          <el-form-item label="模型提供者">
            <el-select v-model="agentForm.model_provider" placeholder="请选择模型提供者" size="small" style="width: 100%;">
              <el-option label="OpenAI" value="openai" />
              <el-option label="Anthropic" value="anthropic" />
              <el-option label="Google" value="google" />
              <el-option label="本地模型" value="local" />
              <el-option label="DeepSeek" value="deepseek" />
              <el-option label="通义千问" value="qwen" />
            </el-select>
          </el-form-item>
          <el-form-item label="模型名称">
            <el-input v-model="agentForm.model_name" placeholder="例如：gpt-4" size="small" />
          </el-form-item>
          <el-form-item label="描述">
            <el-input v-model="agentForm.description" type="textarea" :rows="2" placeholder="请输入描述" size="small" />
          </el-form-item>
          <el-form-item label="提示词模板">
            <el-input v-model="agentForm.prompt_template" type="textarea" :rows="4" placeholder="请输入提示词模板" size="small" />
          </el-form-item>
          <el-form-item label="工具">
            <el-select v-model="agentForm.tools" multiple placeholder="选择工具" size="small" style="width: 100%;">
              <el-option label="网络搜索" value="web_search" />
              <el-option label="文件读取" value="file_read" />
              <el-option label="文件写入" value="file_write" />
              <el-option label="代码执行" value="code_execute" />
              <el-option label="API调用" value="api_call" />
              <el-option label="数据库查询" value="database_query" />
            </el-select>
          </el-form-item>
          <el-form-item label="能力">
            <el-select v-model="agentForm.capabilities" multiple placeholder="选择能力" size="small" style="width: 100%;">
              <el-option label="内容创作" value="content_creation" />
              <el-option label="代码生成" value="code_generation" />
              <el-option label="数据分析" value="data_analysis" />
              <el-option label="设计能力" value="design" />
              <el-option label="销售能力" value="sales" />
              <el-option label="SEO优化" value="seo" />
            </el-select>
          </el-form-item>
        </el-form>
      </el-scrollbar>
      <template #footer>
        <el-button @click="showAddDialog = false" size="small">取消</el-button>
        <el-button type="primary" @click="addAgent" size="small">保存</el-button>
      </template>
    </el-dialog>

    <!-- 编辑代理对话框 -->
    <el-dialog v-model="showEditDialog" title="编辑代理" width="500px" top="5vh">
      <el-scrollbar max-height="60vh">
        <el-form :model="editForm" label-width="100px" label-position="left">
          <el-form-item label="代理名称">
            <el-input v-model="editForm.name" placeholder="请输入代理名称" size="small" />
          </el-form-item>
          <el-form-item label="代理类别">
            <el-select v-model="editForm.category" placeholder="请选择类别" size="small" style="width: 100%;">
              <el-option label="营销" value="marketing" />
              <el-option label="设计" value="design" />
              <el-option label="开发" value="development" />
              <el-option label="销售" value="sales" />
              <el-option label="分析" value="analytics" />
            </el-select>
          </el-form-item>
          <el-form-item label="模型提供者">
            <el-select v-model="editForm.model_provider" placeholder="请选择模型提供者" size="small" style="width: 100%;">
              <el-option label="OpenAI" value="openai" />
              <el-option label="Anthropic" value="anthropic" />
              <el-option label="Google" value="google" />
              <el-option label="本地模型" value="local" />
              <el-option label="DeepSeek" value="deepseek" />
              <el-option label="通义千问" value="qwen" />
            </el-select>
          </el-form-item>
          <el-form-item label="模型名称">
            <el-input v-model="editForm.model_name" placeholder="例如：gpt-4" size="small" />
          </el-form-item>
          <el-form-item label="描述">
            <el-input v-model="editForm.description" type="textarea" :rows="2" placeholder="请输入描述" size="small" />
          </el-form-item>
          <el-form-item label="提示词模板">
            <el-input v-model="editForm.prompt_template" type="textarea" :rows="4" placeholder="请输入提示词模板" size="small" />
          </el-form-item>
          <el-form-item label="工具">
            <el-select v-model="editForm.tools" multiple placeholder="选择工具" size="small" style="width: 100%;">
              <el-option label="网络搜索" value="web_search" />
              <el-option label="文件读取" value="file_read" />
              <el-option label="文件写入" value="file_write" />
              <el-option label="代码执行" value="code_execute" />
              <el-option label="API调用" value="api_call" />
              <el-option label="数据库查询" value="database_query" />
            </el-select>
          </el-form-item>
          <el-form-item label="能力">
            <el-select v-model="editForm.capabilities" multiple placeholder="选择能力" size="small" style="width: 100%;">
              <el-option label="内容创作" value="content_creation" />
              <el-option label="代码生成" value="code_generation" />
              <el-option label="数据分析" value="data_analysis" />
              <el-option label="设计能力" value="design" />
              <el-option label="销售能力" value="sales" />
              <el-option label="SEO优化" value="seo" />
            </el-select>
          </el-form-item>
          <el-form-item label="启用">
            <el-switch v-model="editForm.is_active" />
          </el-form-item>
        </el-form>
      </el-scrollbar>
      <template #footer>
        <el-button @click="showEditDialog = false" size="small">取消</el-button>
        <el-button type="primary" @click="saveAgent" size="small">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Edit, VideoPlay } from '@element-plus/icons-vue'
import api from '@/api'

const agents = ref<any[]>([])
const loading = ref(false)
const categoryFilter = ref('')
const showAddDialog = ref(false)
const showEditDialog = ref(false)
const editingId = ref('')

// 代理表单
const agentForm = ref({
  name: '',
  category: '',
  model_provider: '',
  model_name: '',
  description: '',
  prompt_template: '',
  tools: [] as string[],
  capabilities: [] as string[]
})

// 编辑表单
const editForm = ref({
  name: '',
  category: '',
  model_provider: '',
  model_name: '',
  description: '',
  prompt_template: '',
  tools: [] as string[],
  capabilities: [] as string[],
  is_active: true
})

// 过滤后的代理列表
const filteredAgents = computed(() => {
  if (!categoryFilter.value) return agents.value
  return agents.value.filter(agent => agent.category === categoryFilter.value)
})

onMounted(() => {
  fetchAgents()
})

async function fetchAgents() {
  loading.value = true
  try {
    agents.value = await api.getAgents()
  } catch (error) {
    console.error('获取代理列表失败:', error)
  } finally {
    loading.value = false
  }
}

function getCategoryName(category: string) {
  const names: Record<string, string> = {
    marketing: '营销',
    development: '开发',
    design: '设计',
    sales: '销售',
    analytics: '分析'
  }
  return names[category] || category
}

function getCategoryColor(category: string) {
  const colors: Record<string, string> = {
    marketing: '#67c23a',
    development: '#409eff',
    design: '#e6a23c',
    sales: '#f56c6c',
    analytics: '#9b59b6'
  }
  return colors[category] || '#909399'
}

function getCategoryIcon(category: string) {
  const icons: Record<string, string> = {
    marketing: '📢',
    development: '💻',
    design: '🎨',
    sales: '💰',
    analytics: '📊'
  }
  return icons[category] || '🤖'
}

function editAgent(agent: any) {
  editForm.value = {
    name: agent.name,
    category: agent.category,
    model_provider: agent.model_provider,
    model_name: agent.model_name,
    description: agent.description,
    prompt_template: agent.prompt_template || '',
    tools: agent.tools || [],
    capabilities: agent.capabilities || [],
    is_active: agent.is_active
  }
  editingId.value = agent.id
  showEditDialog.value = true
}

async function saveAgent() {
  try {
    await api.updateAgent(editingId.value, editForm.value)
    ElMessage.success('代理配置已更新')
    showEditDialog.value = false
    await fetchAgents()
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

async function addAgent() {
  try {
    await api.createAgent(agentForm.value)
    ElMessage.success('代理已添加')
    showAddDialog.value = false
    agentForm.value = {
      name: '',
      category: '',
      model_provider: '',
      model_name: '',
      description: '',
      prompt_template: '',
      tools: [],
      capabilities: []
    }
    await fetchAgents()
  } catch (error) {
    ElMessage.error('添加失败')
  }
}

async function toggleAgent(agent: any) {
  try {
    await api.toggleAgent(agent.id)
    ElMessage.success(`代理已${agent.is_active ? '禁用' : '启用'}`)
    await fetchAgents()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

async function testAgent(agent: any) {
  ElMessage.info(`测试代理: ${agent.name}`)
  // TODO: 实现代理测试功能
  setTimeout(() => {
    ElMessage.success('代理测试完成')
  }, 1000)
}
</script>

<style scoped>
.agents-container {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.agent-filters {
  margin-bottom: 16px;
}

.agents-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 16px;
}

.agent-card {
  transition: all 0.3s;
}

.agent-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.agent-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.agent-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}

.card-content {
  margin-bottom: 16px;
}

.card-content p {
  margin-bottom: 8px;
  color: #606266;
  font-size: 14px;
}

.capabilities,
.tools {
  margin-top: 12px;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-top: 4px;
}

.card-footer {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}
</style>
