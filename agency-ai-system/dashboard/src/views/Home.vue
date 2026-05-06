<template>
  <div class="home-container">
    <!-- 顶部导航 -->
    <div class="top-nav">
      <h1>AI多代理系统</h1>
      <div class="nav-actions">
        <el-button @click="viewMode = 'dashboard'" :type="viewMode === 'dashboard' ? 'primary' : ''">
          <el-icon><DataLine /></el-icon>
          仪表盘
        </el-button>
        <el-button @click="viewMode = 'mindmap'" :type="viewMode === 'mindmap' ? 'primary' : ''">
          <el-icon><Share /></el-icon>
          思维导图
        </el-button>
      </div>
    </div>

    <!-- 仪表盘视图 -->
    <div v-if="viewMode === 'dashboard'" class="dashboard-view">
      <!-- 概览卡片 -->
      <div class="overview-cards">
        <el-card class="overview-card">
          <div class="card-body">
            <div class="card-icon" style="background-color: #409eff;">
              <el-icon><Cpu /></el-icon>
            </div>
            <div class="card-info">
              <div class="card-value">{{ systemStatus.cpu_usage || 0 }}%</div>
              <div class="card-label">CPU使用率</div>
            </div>
          </div>
        </el-card>

        <el-card class="overview-card">
          <div class="card-body">
            <div class="card-icon" style="background-color: #67c23a;">
              <el-icon><Coin /></el-icon>
            </div>
            <div class="card-info">
              <div class="card-value">{{ systemStatus.memory_usage || 0 }}%</div>
              <div class="card-label">内存使用率</div>
            </div>
          </div>
        </el-card>

        <el-card class="overview-card">
          <div class="card-body">
            <div class="card-icon" style="background-color: #e6a23c;">
              <el-icon><List /></el-icon>
            </div>
            <div class="card-info">
              <div class="card-value">{{ progressStatus.summary?.running_tasks || 0 }}</div>
              <div class="card-label">运行中任务</div>
            </div>
          </div>
        </el-card>

        <el-card class="overview-card">
          <div class="card-body">
            <div class="card-icon" style="background-color: #f56c6c;">
              <el-icon><User /></el-icon>
            </div>
            <div class="card-info">
              <div class="card-value">{{ agents.length }}</div>
              <div class="card-label">代理数量</div>
            </div>
          </div>
        </el-card>
      </div>

      <!-- 快速操作 -->
      <el-card class="quick-actions">
        <template #header>
          <span>快速操作</span>
        </template>
        <div class="actions-grid">
          <el-button type="primary" @click="$router.push('/tasks')">
            <el-icon><Plus /></el-icon>
            创建任务
          </el-button>
          <el-button type="success" @click="$router.push('/agents')">
            <el-icon><User /></el-icon>
            管理代理
          </el-button>
          <el-button type="warning" @click="$router.push('/models')">
            <el-icon><Cpu /></el-icon>
            配置模型
          </el-button>
          <el-button type="info" @click="$router.push('/logs')">
            <el-icon><Document /></el-icon>
            查看日志
          </el-button>
        </div>
      </el-card>

      <!-- 大脑列表 -->
      <el-card class="brains-list">
        <template #header>
          <div class="card-header">
            <span>大脑列表</span>
            <el-tag type="success">{{ brains.length }} 个</el-tag>
          </div>
        </template>
        <div class="brains-grid">
          <el-card v-for="brain in brains" :key="brain.id" class="brain-card" shadow="hover">
            <div class="brain-info">
              <div class="brain-icon" :style="{ backgroundColor: getBrainColor(brain.brain_type) }">
                <el-icon><Cpu /></el-icon>
              </div>
              <div class="brain-details">
                <h3>{{ brain.name }}</h3>
                <p>{{ brain.description }}</p>
                <div class="brain-meta">
                  <el-tag size="small">{{ brain.brain_type }}</el-tag>
                  <el-tag size="small" type="success">{{ brain.agents?.length || 0 }} 个代理</el-tag>
                </div>
              </div>
            </div>
          </el-card>
        </div>
      </el-card>

      <!-- 代理列表 -->
      <el-card class="agents-list">
        <template #header>
          <div class="card-header">
            <span>代理列表</span>
            <el-tag type="success">{{ agents.length }} 个</el-tag>
          </div>
        </template>
        <div class="agents-grid">
          <el-card v-for="agent in agents" :key="agent.id" class="agent-card" shadow="hover">
            <div class="agent-info">
              <div class="agent-icon" :style="{ backgroundColor: getCategoryColor(agent.category) }">
                {{ getCategoryIcon(agent.category) }}
              </div>
              <div class="agent-details">
                <h3>{{ agent.name }}</h3>
                <p>{{ agent.description }}</p>
                <div class="agent-meta">
                  <el-tag size="small">{{ agent.category }}</el-tag>
                  <el-tag size="small" type="info">{{ agent.model_provider }}/{{ agent.model_name }}</el-tag>
                </div>
              </div>
            </div>
          </el-card>
        </div>
      </el-card>
    </div>

    <!-- 思维导图视图 -->
    <div v-if="viewMode === 'mindmap'" class="mindmap-view">
      <div class="mindmap-container">
        <!-- 工具栏 -->
        <div class="mindmap-toolbar">
          <el-button-group>
            <el-button @click="zoomIn">
              <el-icon><ZoomIn /></el-icon>
            </el-button>
            <el-button @click="zoomOut">
              <el-icon><ZoomOut /></el-icon>
            </el-button>
            <el-button @click="fitView">
              <el-icon><FullScreen /></el-icon>
            </el-button>
            <el-button @click="autoLayout">
              <el-icon><Grid /></el-icon>
            </el-button>
          </el-button-group>
        </div>

        <!-- 图形区域 -->
        <div ref="graphContainer" class="graph-area"></div>

        <!-- 节点详情面板 -->
        <el-drawer v-model="showDetail" title="节点详情" size="400px">
          <div v-if="selectedNode" class="node-detail">
            <el-descriptions :column="1" border>
              <el-descriptions-item label="名称">{{ selectedNode.label }}</el-descriptions-item>
              <el-descriptions-item label="类型">{{ selectedNode.type }}</el-descriptions-item>
              <el-descriptions-item label="状态">
                <el-tag :type="selectedNode.status === 'online' ? 'success' : 'danger'">
                  {{ selectedNode.status }}
                </el-tag>
              </el-descriptions-item>
            </el-descriptions>
          </div>
        </el-drawer>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import cytoscape from 'cytoscape'
import {
  DataLine, Share, Cpu, Coin, List, User, Plus, Document,
  ZoomIn, ZoomOut, FullScreen, Grid
} from '@element-plus/icons-vue'
import api from '@/api'

const viewMode = ref('dashboard')
const graphContainer = ref<HTMLElement>()
const showDetail = ref(false)
const selectedNode = ref<any>(null)
let cy: any = null

// 数据
const systemStatus = ref<any>({})
const progressStatus = ref<any>({})
const agents = ref<any[]>([])
const brains = ref<any[]>([])

let refreshTimer: any = null

onMounted(() => {
  fetchData()
  // 每30秒刷新一次（减少频率）
  refreshTimer = setInterval(fetchData, 30000)
})

onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
  if (cy) {
    cy.destroy()
  }
})

// 监听视图模式变化
watch(viewMode, (newMode) => {
  if (newMode === 'mindmap') {
    nextTick(() => {
      initMindMap()
    })
  }
})

async function fetchData() {
  try {
    // 并行请求，提高加载速度
    const [system, progress, agentsData, brainsData] = await Promise.all([
      api.getSystemStatus(),
      api.getProgressReport(),
      api.getAgents(),
      api.getBrains()
    ])
    systemStatus.value = system
    progressStatus.value = progress
    agents.value = agentsData
    brains.value = brainsData
  } catch (error) {
    console.error('获取数据失败:', error)
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

function initMindMap() {
  if (!graphContainer.value) return

  // 准备节点数据
  const nodes: any[] = []
  const edges: any[] = []

  // 添加主大脑节点
  nodes.push({
    data: { id: 'master', label: '主大脑', type: 'brain', status: 'online' }
  })

  // 添加子大脑节点
  brains.value.forEach((brain: any) => {
    if (brain.brain_type !== 'master') {
      nodes.push({
        data: {
          id: brain.id,
          label: brain.name,
          type: 'brain',
          status: brain.is_active ? 'online' : 'offline',
          brain_type: brain.brain_type
        }
      })
      edges.push({
        data: { source: 'master', target: brain.id, type: 'control' }
      })
    }
  })

  // 添加代理节点
  agents.value.forEach((agent: any) => {
    nodes.push({
      data: {
        id: agent.id,
        label: agent.name,
        type: 'agent',
        status: agent.is_active ? 'online' : 'offline',
        category: agent.category
      }
    })
    // 连接到对应的大脑
    const brain = brains.value.find((b: any) =>
      b.agents?.includes(agent.name.toLowerCase().replace(/\s+/g, '_'))
    )
    if (brain) {
      edges.push({
        data: { source: brain.id, target: agent.id, type: 'agent' }
      })
    }
  })

  cy = cytoscape({
    container: graphContainer.value,
    elements: [...nodes, ...edges],
    style: [
      {
        selector: 'node[type="brain"]',
        style: {
          'background-color': '#409eff',
          'shape': 'round-rectangle',
          'width': 80,
          'height': 60,
          'label': 'data(label)',
          'font-size': '14px',
          'font-weight': 'bold',
          'color': '#fff',
          'text-valign': 'center',
          'text-halign': 'center',
        }
      },
      {
        selector: 'node[type="agent"]',
        style: {
          'background-color': '#67c23a',
          'shape': 'ellipse',
          'width': 60,
          'height': 60,
          'label': 'data(label)',
          'font-size': '12px',
          'color': '#fff',
          'text-valign': 'center',
          'text-halign': 'center',
        }
      },
      {
        selector: 'node[status="offline"]',
        style: {
          'background-color': '#909399',
        }
      },
      {
        selector: 'edge[type="control"]',
        style: {
          'width': 3,
          'line-color': '#409eff',
          'target-arrow-color': '#409eff',
          'target-arrow-shape': 'triangle',
          'curve-style': 'bezier',
        }
      },
      {
        selector: 'edge[type="agent"]',
        style: {
          'width': 2,
          'line-color': '#67c23a',
          'target-arrow-color': '#67c23a',
          'target-arrow-shape': 'triangle',
          'curve-style': 'bezier',
        }
      }
    ],
    layout: {
      name: 'breadthfirst',
      directed: true,
      roots: '#master',
      spacingFactor: 1.5,
    }
  })

  // 点击事件
  cy.on('tap', 'node', (evt: any) => {
    selectedNode.value = evt.target.data()
    showDetail.value = true
  })

  // 点击空白区域关闭详情
  cy.on('tap', (evt: any) => {
    if (evt.target === cy) {
      showDetail.value = false
      selectedNode.value = null
    }
  })
}

function zoomIn() {
  if (cy) cy.zoom(cy.zoom() * 1.2)
}

function zoomOut() {
  if (cy) cy.zoom(cy.zoom() / 1.2)
}

function fitView() {
  if (cy) cy.fit()
}

function autoLayout() {
  if (cy) {
    cy.layout({
      name: 'breadthfirst',
      directed: true,
      roots: '#master',
      spacingFactor: 1.5,
    }).run()
  }
}
</script>

<style scoped>
.home-container {
  max-width: 1400px;
  margin: 0 auto;
}

.top-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.top-nav h1 {
  margin: 0;
  color: #303133;
}

.nav-actions {
  display: flex;
  gap: 8px;
}

/* 仪表盘视图 */
.dashboard-view {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.overview-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
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
  font-size: 28px;
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

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

/* 大脑列表 */
.brains-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.brain-card {
  cursor: pointer;
  transition: all 0.3s;
}

.brain-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.brain-info {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.brain-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.brain-icon .el-icon {
  font-size: 24px;
  color: #fff;
}

.brain-details h3 {
  margin: 0 0 8px 0;
  font-size: 16px;
  color: #303133;
}

.brain-details p {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #606266;
}

.brain-meta {
  display: flex;
  gap: 8px;
}

/* 代理列表 */
.agents-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.agent-card {
  cursor: pointer;
  transition: all 0.3s;
}

.agent-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.agent-info {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.agent-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  flex-shrink: 0;
}

.agent-details h3 {
  margin: 0 0 8px 0;
  font-size: 16px;
  color: #303133;
}

.agent-details p {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #606266;
}

.agent-meta {
  display: flex;
  gap: 8px;
}

/* 思维导图视图 */
.mindmap-view {
  height: calc(100vh - 200px);
}

.mindmap-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: #fff;
  border-radius: 8px;
  overflow: hidden;
}

.mindmap-toolbar {
  padding: 16px;
  border-bottom: 1px solid #e4e7ed;
}

.graph-area {
  flex: 1;
  background-color: #f5f7fa;
}

.node-detail {
  padding: 16px;
}
</style>
