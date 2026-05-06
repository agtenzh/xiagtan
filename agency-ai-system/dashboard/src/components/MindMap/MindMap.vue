<template>
  <div class="ai-mindmap-container">
    <!-- 背景粒子效果 -->
    <canvas ref="particleCanvas" class="particle-canvas"></canvas>

    <!-- 工具栏 -->
    <div class="ai-toolbar">
      <div class="toolbar-left">
        <div class="logo-section">
          <div class="neural-icon">
            <div class="neural-node"></div>
            <div class="neural-node"></div>
            <div class="neural-node"></div>
          </div>
          <span class="logo-text">AI Neural Network</span>
        </div>
      </div>

      <div class="toolbar-center">
        <div class="control-panel">
          <button class="neural-btn" @click="zoomIn" title="放大">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle cx="11" cy="11" r="8"/>
              <path d="m21 21-4.35-4.35"/>
              <path d="M11 8v6M8 11h6"/>
            </svg>
          </button>
          <button class="neural-btn" @click="zoomOut" title="缩小">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle cx="11" cy="11" r="8"/>
              <path d="m21 21-4.35-4.35M8 11h6"/>
            </svg>
          </button>
          <button class="neural-btn" @click="fitView" title="适应屏幕">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/>
            </svg>
          </button>
          <button class="neural-btn" @click="toggleAutoRotate" :class="{ active: autoRotate }" title="自动旋转">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
              <path d="M21 3v5h-5"/>
            </svg>
          </button>
        </div>
      </div>

      <div class="toolbar-right">
        <button class="glow-btn" @click="addBrain">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M12 5v14M5 12h14"/>
          </svg>
          <span>添加节点</span>
        </button>
      </div>
    </div>

    <!-- 思维导图区域 -->
    <div ref="graphContainer" class="neural-network"></div>

    <!-- 节点统计面板 -->
    <div class="stats-panel">
      <div class="stat-item">
        <div class="stat-icon brain-icon">
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2a9 9 0 0 1 9 9c0 3.1-1.6 5.8-4 7.4V22h-2v-2.5c-.6.3-1.3.5-2 .5-2.2 0-4-1.8-4-4s1.8-4 4-4c.7 0 1.4.2 2 .5V22h-2v-3.6c-2.4-1.6-4-4.3-4-7.4a9 9 0 0 1 9-9zm-3 9a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm6 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2z"/>
          </svg>
        </div>
        <div class="stat-info">
          <div class="stat-value">{{ brainNodes.length }}</div>
          <div class="stat-label">大脑节点</div>
        </div>
      </div>

      <div class="stat-item">
        <div class="stat-icon agent-icon">
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
          </svg>
        </div>
        <div class="stat-info">
          <div class="stat-value">{{ agentNodes.length }}</div>
          <div class="stat-label">代理节点</div>
        </div>
      </div>

      <div class="stat-item">
        <div class="stat-icon online-icon">
          <svg viewBox="0 0 24 24" fill="currentColor">
            <circle cx="12" cy="12" r="4"/>
          </svg>
        </div>
        <div class="stat-info">
          <div class="stat-value">{{ onlineCount }}</div>
          <div class="stat-label">在线节点</div>
        </div>
      </div>
    </div>

    <!-- 节点详情面板 -->
    <Transition name="slide">
      <div v-if="showDetail" class="detail-panel">
        <div class="detail-header">
          <h3>节点详情</h3>
          <button class="close-btn" @click="showDetail = false">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M18 6L6 18M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <div class="detail-content" v-if="selectedNode">
          <div class="node-visual">
            <div class="neural-glow" :class="selectedNode.type"></div>
            <div class="node-icon">
              <svg v-if="selectedNode.type === 'brain'" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2a9 9 0 0 1 9 9c0 3.1-1.6 5.8-4 7.4V22h-2v-2.5c-.6.3-1.3.5-2 .5-2.2 0-4-1.8-4-4s1.8-4 4-4c.7 0 1.4.2 2 .5V22h-2v-3.6c-2.4-1.6-4-4.3-4-7.4a9 9 0 0 1 9-9z"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
              </svg>
            </div>
          </div>

          <div class="detail-info">
            <div class="info-row">
              <span class="info-label">名称</span>
              <span class="info-value">{{ selectedNode.label }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">类型</span>
              <span class="info-value type-badge" :class="selectedNode.type">
                {{ selectedNode.type === 'brain' ? '大脑' : '代理' }}
              </span>
            </div>
            <div class="info-row">
              <span class="info-label">状态</span>
              <span class="status-indicator" :class="selectedNode.status">
                <span class="status-dot"></span>
                {{ selectedNode.status === 'online' ? '在线' : '离线' }}
              </span>
            </div>
            <div class="info-row" v-if="selectedNode.type === 'agent'">
              <span class="info-label">所属大脑</span>
              <span class="info-value">{{ selectedNode.brain || '-' }}</span>
            </div>
          </div>

          <div class="detail-actions">
            <button class="action-btn primary">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
              </svg>
              编辑
            </button>
            <button class="action-btn" :class="selectedNode.status === 'online' ? 'danger' : 'success'">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path v-if="selectedNode.status === 'online'" d="M18.36 6.64a9 9 0 1 1-12.73 0M12 2v10"/>
                <path v-else d="M12 2a9 9 0 0 1 9 9M12 2a9 9 0 0 0-9 9M12 22v-6"/>
              </svg>
              {{ selectedNode.status === 'online' ? '下线' : '上线' }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import cytoscape from 'cytoscape'
import dagre from 'cytoscape-dagre'

cytoscape.use(dagre)

const graphContainer = ref<HTMLElement>()
const particleCanvas = ref<HTMLElement>()
const showDetail = ref(false)
const selectedNode = ref<any>(null)
const autoRotate = ref(false)
let cy: any = null
let particles: any = null
let animationId: number | null = null

const brainNodes = computed(() => {
  if (!cy) return []
  return cy.nodes('[type="brain"]').map((node: any) => node.data())
})

const agentNodes = computed(() => {
  if (!cy) return []
  return cy.nodes('[type="agent"]').map((node: any) => node.data())
})

const onlineCount = computed(() => {
  if (!cy) return 0
  return cy.nodes('[status="online"]').length
})

onMounted(() => {
  initGraph()
  initParticles()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  if (cy) cy.destroy()
  if (animationId) cancelAnimationFrame(animationId)
  window.removeEventListener('resize', handleResize)
})

function initGraph() {
  if (!graphContainer.value) return

  cy = cytoscape({
    container: graphContainer.value,
    elements: [
      { data: { id: 'master', label: '主大脑', type: 'brain', status: 'online', level: 0 } },
      { data: { id: 'marketing', label: '营销大脑', type: 'brain', status: 'online', level: 1 } },
      { data: { id: 'development', label: '开发大脑', type: 'brain', status: 'online', level: 1 } },
      { data: { id: 'design', label: '设计大脑', type: 'brain', status: 'offline', level: 1 } },
      { data: { id: 'sales', label: '销售大脑', type: 'brain', status: 'online', level: 1 } },
      { data: { id: 'analytics', label: '分析大脑', type: 'brain', status: 'online', level: 1 } },
      { data: { id: 'content_creator', label: '内容创作', type: 'agent', brain: 'marketing', status: 'online', level: 2 } },
      { data: { id: 'seo_expert', label: 'SEO专家', type: 'agent', brain: 'marketing', status: 'online', level: 2 } },
      { data: { id: 'code_generator', label: '代码生成', type: 'agent', brain: 'development', status: 'online', level: 2 } },
      { data: { id: 'test_writer', label: '测试编写', type: 'agent', brain: 'development', status: 'online', level: 2 } },
      { data: { id: 'ui_designer', label: 'UI设计', type: 'agent', brain: 'design', status: 'offline', level: 2 } },
      { data: { id: 'visual_designer', label: '视觉设计', type: 'agent', brain: 'design', status: 'offline', level: 2 } },
      { data: { id: 'social_media', label: '社交媒体', type: 'agent', brain: 'marketing', status: 'online', level: 2 } },
      { data: { id: 'data_analyst', label: '数据分析', type: 'agent', brain: 'analytics', status: 'online', level: 2 } },
      { data: { id: 'sales_strategist', label: '销售策略', type: 'agent', brain: 'sales', status: 'online', level: 2 } },
      { data: { source: 'master', target: 'marketing', type: 'control' } },
      { data: { source: 'master', target: 'development', type: 'control' } },
      { data: { source: 'master', target: 'design', type: 'control' } },
      { data: { source: 'master', target: 'sales', type: 'control' } },
      { data: { source: 'master', target: 'analytics', type: 'control' } },
      { data: { source: 'marketing', target: 'content_creator', type: 'agent' } },
      { data: { source: 'marketing', target: 'seo_expert', type: 'agent' } },
      { data: { source: 'marketing', target: 'social_media', type: 'agent' } },
      { data: { source: 'development', target: 'code_generator', type: 'agent' } },
      { data: { source: 'development', target: 'test_writer', type: 'agent' } },
      { data: { source: 'design', target: 'ui_designer', type: 'agent' } },
      { data: { source: 'design', target: 'visual_designer', type: 'agent' } },
      { data: { source: 'analytics', target: 'data_analyst', type: 'agent' } },
      { data: { source: 'sales', target: 'sales_strategist', type: 'agent' } },
    ],
    style: [
      {
        selector: 'node[type="brain"]',
        style: {
          'label': 'data(label)',
          'text-valign': 'center',
          'text-halign': 'center',
          'color': '#00f5ff',
          'font-size': 13,
          'font-weight': 700,
          'font-family': 'Rajdhani, sans-serif',
          'text-outline-width': 3,
          'text-outline-color': '#0a0a0f',
          'text-wrap': 'ellipsis',
          'text-max-width': '90px',
          'width': 100,
          'height': 100,
          'shape': 'ellipse',
          'background-color': '#0d1b3e',
          'background-blacken': 0.3,
        }
      },
      {
        selector: 'node[type="agent"]',
        style: {
          'label': 'data(label)',
          'text-valign': 'center',
          'text-halign': 'center',
          'color': '#c4b5fd',
          'font-size': 11,
          'font-weight': 600,
          'font-family': 'Rajdhani, sans-serif',
          'text-outline-width': 2,
          'text-outline-color': '#0a0a0f',
          'text-wrap': 'ellipsis',
          'text-max-width': '55px',
          'width': 60,
          'height': 60,
          'shape': 'round-hexagon',
        }
      },
      {
        selector: 'node[status="online"]',
        style: {
          'border-width': 3,
          'border-color': '#00f5ff',
          'background-color': '#0d1b3e',
          'box-shadow-color': '#00f5ff',
          'box-shadow-opacity': 0.3,
          'box-shadow-blur': 15,
          'box-shadow-spread': 3,
        }
      },
      {
        selector: 'node[status="offline"]',
        style: {
          'border-width': 2,
          'border-color': '#ff4757',
          'background-color': '#1a1020',
          'opacity': 0.7,
        }
      },
      {
        selector: 'node:selected',
        style: {
          'border-width': 4,
          'border-color': '#ff00ff',
          'overlay-opacity': 0.1,
          'overlay-color': '#ff00ff',
        }
      },
      {
        selector: 'edge',
        style: {
          'width': 2,
          'line-style': 'dashed',
          'curve-style': 'bezier',
          'target-arrow-shape': 'triangle',
          'target-arrow-width': 8,
          'line-opacity': 0.6,
        }
      },
      {
        selector: 'edge[type="control"]',
        style: {
          'line-color': '#00f5ff',
          'target-arrow-color': '#00f5ff',
          'width': 3,
          'line-style': 'solid',
        }
      },
      {
        selector: 'edge[type="agent"]',
        style: {
          'line-color': '#7c3aed',
          'target-arrow-color': '#7c3aed',
          'width': 2,
        }
      },
    ],
    layout: {
      name: 'dagre',
      rankDir: 'TB',
      nodeSep: 80,
      rankSep: 120,
      padding: 50,
    },
    minZoom: 0.3,
    maxZoom: 3,
    wheelSensitivity: 0.3,
  })

  cy.on('tap', 'node', (evt: any) => {
    selectedNode.value = evt.target.data()
    showDetail.value = true
  })

  cy.on('tap', (evt: any) => {
    if (evt.target === cy) {
      showDetail.value = false
      selectedNode.value = null
    }
  })

  cy.on('mouseover', 'node', (evt: any) => {
    const node = evt.target
    node.animate({
      style: {
        'border-width': 5,
        'border-color': '#ff00ff',
      }
    }, {
      duration: 200,
      easing: 'ease-out'
    })
  })

  cy.on('mouseout', 'node', (evt: any) => {
    const node = evt.target
    const status = node.data('status')
    node.animate({
      style: {
        'border-width': status === 'online' ? 3 : 2,
        'border-color': status === 'online' ? '#00f5ff' : '#ff4757',
      }
    }, {
      duration: 200,
      easing: 'ease-out'
    })
  })
}

function initParticles() {
  if (!particleCanvas.value) return

  const canvas = particleCanvas.value
  const ctx = canvas.getContext('2d')
  if (!ctx) return

  function resize() {
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight
  }
  resize()
  window.addEventListener('resize', resize)

  const particleArray: any[] = []
  const particleCount = 80

  for (let i = 0; i < particleCount; i++) {
    particleArray.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 0.5,
      vy: (Math.random() - 0.5) * 0.5,
      radius: Math.random() * 2 + 1,
      color: Math.random() > 0.5 ? '#00f5ff' : '#7c3aed',
      alpha: Math.random() * 0.5 + 0.2,
    })
  }

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height)

    particleArray.forEach((p, i) => {
      p.x += p.vx
      p.y += p.vy

      if (p.x < 0 || p.x > canvas.width) p.vx *= -1
      if (p.y < 0 || p.y > canvas.height) p.vy *= -1

      ctx.beginPath()
      ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2)
      ctx.fillStyle = p.color
      ctx.globalAlpha = p.alpha
      ctx.fill()

      particleArray.forEach((p2, j) => {
        if (i === j) return
        const dx = p.x - p2.x
        const dy = p.y - p2.y
        const dist = Math.sqrt(dx * dx + dy * dy)

        if (dist < 150) {
          ctx.beginPath()
          ctx.moveTo(p.x, p.y)
          ctx.lineTo(p2.x, p2.y)
          ctx.strokeStyle = p.color
          ctx.globalAlpha = 0.1 * (1 - dist / 150)
          ctx.lineWidth = 1
          ctx.stroke()
        }
      })
    })

    ctx.globalAlpha = 1
    animationId = requestAnimationFrame(animate)
  }

  animate()
}

function handleResize() {
  if (cy) cy.resize()
}

function zoomIn() {
  if (cy) cy.zoom(cy.zoom() * 1.2)
}

function zoomOut() {
  if (cy) cy.zoom(cy.zoom() / 1.2)
}

function fitView() {
  if (cy) cy.fit(undefined, 50)
}

function toggleAutoRotate() {
  autoRotate.value = !autoRotate.value
}

function addBrain() {
  console.log('添加节点')
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700&family=Rajdhani:wght@300;400;500;600;700&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.ai-mindmap-container {
  position: relative;
  width: 100%;
  height: 100vh;
  background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #0a0a0f 100%);
  overflow: hidden;
  font-family: 'Rajdhani', sans-serif;
}

.particle-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  pointer-events: none;
}

/* Toolbar Styles */
.ai-toolbar {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 30px;
  background: linear-gradient(180deg, rgba(10, 10, 15, 0.95) 0%, rgba(10, 10, 15, 0) 100%);
  z-index: 10;
  border-bottom: 1px solid rgba(0, 245, 255, 0.1);
}

.toolbar-left {
  display: flex;
  align-items: center;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 15px;
}

.neural-icon {
  position: relative;
  width: 50px;
  height: 50px;
}

.neural-node {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(135deg, #00f5ff 0%, #7c3aed 100%);
  animation: pulse 2s ease-in-out infinite;
}

.neural-node:nth-child(1) {
  width: 20px;
  height: 20px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: 0s;
}

.neural-node:nth-child(2) {
  width: 12px;
  height: 12px;
  top: 10%;
  left: 20%;
  animation-delay: 0.3s;
}

.neural-node:nth-child(3) {
  width: 12px;
  height: 12px;
  bottom: 10%;
  right: 20%;
  animation-delay: 0.6s;
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.6;
    transform: scale(1);
    box-shadow: 0 0 20px rgba(0, 245, 255, 0.5);
  }
  50% {
    opacity: 1;
    transform: scale(1.1);
    box-shadow: 0 0 40px rgba(0, 245, 255, 0.8);
  }
}

.logo-text {
  font-family: 'Orbitron', sans-serif;
  font-size: 24px;
  font-weight: 700;
  background: linear-gradient(90deg, #00f5ff, #7c3aed, #ff00ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-transform: uppercase;
  letter-spacing: 3px;
}

.toolbar-center {
  display: flex;
  align-items: center;
}

.control-panel {
  display: flex;
  gap: 10px;
  padding: 8px;
  background: rgba(26, 26, 46, 0.8);
  border: 1px solid rgba(0, 245, 255, 0.2);
  border-radius: 12px;
  backdrop-filter: blur(10px);
}

.neural-btn {
  width: 44px;
  height: 44px;
  border: 1px solid rgba(0, 245, 255, 0.3);
  border-radius: 8px;
  background: linear-gradient(135deg, rgba(0, 245, 255, 0.1) 0%, rgba(124, 58, 237, 0.1) 100%);
  color: #00f5ff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.neural-btn svg {
  width: 20px;
  height: 20px;
}

.neural-btn:hover {
  background: linear-gradient(135deg, rgba(0, 245, 255, 0.3) 0%, rgba(124, 58, 237, 0.3) 100%);
  border-color: #00f5ff;
  box-shadow: 0 0 20px rgba(0, 245, 255, 0.3);
  transform: translateY(-2px);
}

.neural-btn.active {
  background: linear-gradient(135deg, #00f5ff 0%, #7c3aed 100%);
  color: #fff;
  border-color: transparent;
}

.toolbar-right {
  display: flex;
  align-items: center;
}

.glow-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 24px;
  border: 2px solid #00f5ff;
  border-radius: 25px;
  background: transparent;
  color: #00f5ff;
  font-family: 'Orbitron', sans-serif;
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 2px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.glow-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0, 245, 255, 0.3), transparent);
  transition: left 0.5s ease;
}

.glow-btn:hover::before {
  left: 100%;
}

.glow-btn:hover {
  background: linear-gradient(135deg, rgba(0, 245, 255, 0.2) 0%, rgba(124, 58, 237, 0.2) 100%);
  box-shadow: 0 0 30px rgba(0, 245, 255, 0.4);
  transform: translateY(-2px);
}

.glow-btn svg {
  width: 18px;
  height: 18px;
}

/* Neural Network Area */
.neural-network {
  position: absolute;
  top: 80px;
  left: 0;
  right: 0;
  bottom: 80px;
  z-index: 5;
  background: radial-gradient(ellipse at center, rgba(124, 58, 237, 0.1) 0%, transparent 70%);
}

/* Stats Panel */
.stats-panel {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 20px;
  padding: 20px 40px;
  background: rgba(10, 10, 15, 0.9);
  border: 1px solid rgba(0, 245, 255, 0.2);
  border-radius: 20px;
  backdrop-filter: blur(20px);
  z-index: 10;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 15px;
}

.stat-icon {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  background: rgba(0, 245, 255, 0.1);
  border: 1px solid rgba(0, 245, 255, 0.3);
}

.stat-icon svg {
  width: 28px;
  height: 28px;
}

.brain-icon {
  color: #00f5ff;
  background: linear-gradient(135deg, rgba(0, 245, 255, 0.2) 0%, rgba(124, 58, 237, 0.2) 100%);
}

.agent-icon {
  color: #7c3aed;
  background: linear-gradient(135deg, rgba(124, 58, 237, 0.2) 0%, rgba(255, 0, 255, 0.2) 100%);
}

.online-icon {
  color: #10b981;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(0, 245, 255, 0.2) 100%);
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-family: 'Orbitron', sans-serif;
  font-size: 28px;
  font-weight: 700;
  color: #fff;
  line-height: 1;
}

.stat-label {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.6);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-top: 4px;
}

/* Detail Panel */
.detail-panel {
  position: absolute;
  top: 100px;
  right: 30px;
  width: 380px;
  background: rgba(10, 10, 15, 0.95);
  border: 1px solid rgba(0, 245, 255, 0.3);
  border-radius: 20px;
  backdrop-filter: blur(20px);
  z-index: 20;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5), 0 0 40px rgba(0, 245, 255, 0.1);
}

.detail-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px;
  background: linear-gradient(180deg, rgba(0, 245, 255, 0.1) 0%, transparent 100%);
  border-bottom: 1px solid rgba(0, 245, 255, 0.1);
}

.detail-header h3 {
  font-family: 'Orbitron', sans-serif;
  font-size: 18px;
  font-weight: 600;
  color: #00f5ff;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.close-btn {
  width: 36px;
  height: 36px;
  border: 1px solid rgba(255, 71, 87, 0.5);
  border-radius: 50%;
  background: rgba(255, 71, 87, 0.1);
  color: #ff4757;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.close-btn svg {
  width: 18px;
  height: 18px;
}

.close-btn:hover {
  background: #ff4757;
  color: #fff;
  border-color: #ff4757;
  transform: rotate(90deg);
}

.detail-content {
  padding: 30px;
}

.node-visual {
  position: relative;
  width: 120px;
  height: 120px;
  margin: 0 auto 30px;
}

.neural-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: linear-gradient(135deg, #00f5ff 0%, #7c3aed 100%);
  animation: glow-pulse 2s ease-in-out infinite;
  opacity: 0.3;
  filter: blur(20px);
}

.neural-glow.brain {
  background: linear-gradient(135deg, #00f5ff 0%, #7c3aed 100%);
}

.neural-glow.agent {
  background: linear-gradient(135deg, #7c3aed 0%, #ff00ff 100%);
}

@keyframes glow-pulse {
  0%, 100% {
    opacity: 0.3;
    transform: translate(-50%, -50%) scale(1);
  }
  50% {
    opacity: 0.6;
    transform: translate(-50%, -50%) scale(1.1);
  }
}

.node-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #0a1628 0%, #1a1a2e 100%);
  border: 3px solid #00f5ff;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #00f5ff;
  box-shadow: 0 0 30px rgba(0, 245, 255, 0.4);
}

.node-icon svg {
  width: 40px;
  height: 40px;
}

.detail-info {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 30px;
}

.info-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.info-label {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.6);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.info-value {
  font-family: 'Orbitron', sans-serif;
  font-size: 16px;
  font-weight: 600;
  color: #fff;
}

.type-badge {
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 13px;
}

.type-badge.brain {
  background: linear-gradient(135deg, rgba(0, 245, 255, 0.2) 0%, rgba(124, 58, 237, 0.2) 100%);
  border: 1px solid rgba(0, 245, 255, 0.5);
  color: #00f5ff;
}

.type-badge.agent {
  background: linear-gradient(135deg, rgba(124, 58, 237, 0.2) 0%, rgba(255, 0, 255, 0.2) 100%);
  border: 1px solid rgba(124, 58, 237, 0.5);
  color: #7c3aed;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'Orbitron', sans-serif;
  font-size: 14px;
  font-weight: 600;
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  animation: blink 1.5s ease-in-out infinite;
}

.status-indicator.online {
  color: #10b981;
}

.status-indicator.online .status-dot {
  background: #10b981;
  box-shadow: 0 0 10px rgba(16, 185, 129, 0.6);
}

.status-indicator.offline {
  color: #ff4757;
}

.status-indicator.offline .status-dot {
  background: #ff4757;
  box-shadow: 0 0 10px rgba(255, 71, 87, 0.6);
}

@keyframes blink {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.detail-actions {
  display: flex;
  gap: 12px;
}

.action-btn {
  flex: 1;
  padding: 14px;
  border: 1px solid rgba(0, 245, 255, 0.3);
  border-radius: 12px;
  background: rgba(0, 245, 255, 0.1);
  color: #00f5ff;
  font-family: 'Rajdhani', sans-serif;
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.action-btn svg {
  width: 18px;
  height: 18px;
}

.action-btn:hover {
  background: rgba(0, 245, 255, 0.2);
  border-color: #00f5ff;
  transform: translateY(-2px);
  box-shadow: 0 5px 20px rgba(0, 245, 255, 0.2);
}

.action-btn.primary {
  background: linear-gradient(135deg, #00f5ff 0%, #7c3aed 100%);
  border-color: transparent;
  color: #fff;
}

.action-btn.primary:hover {
  box-shadow: 0 5px 30px rgba(0, 245, 255, 0.4);
}

.action-btn.success {
  background: rgba(16, 185, 129, 0.1);
  border-color: rgba(16, 185, 129, 0.5);
  color: #10b981;
}

.action-btn.success:hover {
  background: rgba(16, 185, 129, 0.2);
  box-shadow: 0 5px 20px rgba(16, 185, 129, 0.2);
}

.action-btn.danger {
  background: rgba(255, 71, 87, 0.1);
  border-color: rgba(255, 71, 87, 0.5);
  color: #ff4757;
}

.action-btn.danger:hover {
  background: rgba(255, 71, 87, 0.2);
  box-shadow: 0 5px 20px rgba(255, 71, 87, 0.2);
}

/* Transitions */
.slide-enter-active,
.slide-leave-active {
  transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.slide-enter-from {
  transform: translateX(100px);
  opacity: 0;
}

.slide-leave-to {
  transform: translateX(100px);
  opacity: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .ai-toolbar {
    padding: 0 15px;
  }

  .logo-text {
    font-size: 18px;
  }

  .stats-panel {
    padding: 15px 20px;
    gap: 15px;
  }

  .stat-value {
    font-size: 22px;
  }

  .detail-panel {
    width: calc(100% - 60px);
    right: 30px;
  }
}
</style>
