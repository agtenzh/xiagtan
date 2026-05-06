<template>
  <el-config-provider :locale="zhCn">
    <div class="app-container">
      <!-- 侧边栏 -->
      <el-aside width="260px" class="app-aside">
        <div class="logo">
          <div class="logo-icon">
            <div class="neural-ring"></div>
            <div class="neural-ring"></div>
            <div class="neural-ring"></div>
          </div>
          <h2>AI Agents</h2>
        </div>

        <el-menu
          :default-active="currentRoute"
          router
          class="aside-menu"
        >
          <el-menu-item index="/">
            <el-icon><HomeFilled /></el-icon>
            <span>首页</span>
          </el-menu-item>
          <el-menu-item index="/dashboard">
            <el-icon><DataLine /></el-icon>
            <span>神经网络</span>
          </el-menu-item>
          <el-menu-item index="/monitor">
            <el-icon><Odometer /></el-icon>
            <span>系统监控</span>
          </el-menu-item>
          <el-menu-item index="/agents">
            <el-icon><User /></el-icon>
            <span>代理管理</span>
          </el-menu-item>
          <el-menu-item index="/models">
            <el-icon><Cpu /></el-icon>
            <span>模型配置</span>
          </el-menu-item>
          <el-menu-item index="/tasks">
            <el-icon><List /></el-icon>
            <span>任务管理</span>
          </el-menu-item>
          <el-menu-item index="/logs">
            <el-icon><Document /></el-icon>
            <span>日志查看</span>
          </el-menu-item>
          <el-menu-item index="/config">
            <el-icon><Setting /></el-icon>
            <span>配置管理</span>
          </el-menu-item>
          <el-menu-item index="/settings">
            <el-icon><Tools /></el-icon>
            <span>系统设置</span>
          </el-menu-item>
        </el-menu>

        <div class="sidebar-footer">
          <div class="system-status">
            <div class="status-indicator online">
              <span class="status-dot"></span>
              <span class="status-text">系统在线</span>
            </div>
          </div>
        </div>
      </el-aside>

      <!-- 主内容区 -->
      <el-main class="app-main">
        <router-view />
      </el-main>
    </div>
  </el-config-provider>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import {
  HomeFilled,
  User,
  Cpu,
  List,
  Document,
  Setting,
  Tools,
  DataLine,
  Odometer
} from '@element-plus/icons-vue'

const route = useRoute()
const currentRoute = computed(() => route.path)
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700&family=Rajdhani:wght@300;400;500;600;700&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --primary-cyan: #00f5ff;
  --primary-purple: #7c3aed;
  --primary-magenta: #ff00ff;
  --bg-dark: #0a0a0f;
  --bg-secondary: #1a1a2e;
  --text-primary: #ffffff;
  --text-secondary: rgba(255, 255, 255, 0.7);
  --border-color: rgba(0, 245, 255, 0.2);
}

body {
  font-family: 'Rajdhani', sans-serif;
  background: var(--bg-dark);
  color: var(--text-primary);
}

.app-container {
  display: flex;
  height: 100vh;
  background: linear-gradient(135deg, var(--bg-dark) 0%, var(--bg-secondary) 50%, var(--bg-dark) 100%);
}

.app-aside {
  background: linear-gradient(180deg, rgba(10, 10, 15, 0.98) 0%, rgba(26, 26, 46, 0.98) 100%);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

.app-aside::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 200px;
  background: radial-gradient(ellipse at top, rgba(0, 245, 255, 0.05) 0%, transparent 70%);
  pointer-events: none;
}

.logo {
  height: 100px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 20px;
  border-bottom: 1px solid var(--border-color);
  position: relative;
  z-index: 1;
}

.logo-icon {
  position: relative;
  width: 50px;
  height: 50px;
}

.neural-ring {
  position: absolute;
  border-radius: 50%;
  border: 2px solid var(--primary-cyan);
  animation: ring-pulse 3s ease-in-out infinite;
}

.neural-ring:nth-child(1) {
  width: 50px;
  height: 50px;
  top: 0;
  left: 0;
  animation-delay: 0s;
}

.neural-ring:nth-child(2) {
  width: 35px;
  height: 35px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border-color: var(--primary-purple);
  animation-delay: 0.5s;
}

.neural-ring:nth-child(3) {
  width: 20px;
  height: 20px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: linear-gradient(135deg, var(--primary-cyan) 0%, var(--primary-purple) 100%);
  animation-delay: 1s;
  border: none;
}

@keyframes ring-pulse {
  0%, 100% {
    opacity: 0.3;
    transform: scale(1);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.1);
  }
}

.logo h2 {
  font-family: 'Orbitron', sans-serif;
  font-size: 16px;
  font-weight: 700;
  background: linear-gradient(90deg, var(--primary-cyan), var(--primary-purple));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-transform: uppercase;
  letter-spacing: 3px;
}

.aside-menu {
  flex: 1;
  border-right: none;
  background: transparent;
  padding: 20px 0;
}

.aside-menu .el-menu-item {
  color: var(--text-secondary);
  margin: 8px 16px;
  padding-left: 20px !important;
  border-radius: 12px;
  height: 52px;
  font-size: 15px;
  font-weight: 500;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.aside-menu .el-menu-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 0;
  height: 100%;
  background: linear-gradient(90deg, rgba(0, 245, 255, 0.1) 0%, transparent 100%);
  transition: width 0.3s ease;
}

.aside-menu .el-menu-item:hover {
  color: var(--primary-cyan);
  background: transparent;
}

.aside-menu .el-menu-item:hover::before {
  width: 100%;
}

.aside-menu .el-menu-item.is-active {
  color: var(--primary-cyan);
  background: linear-gradient(90deg, rgba(0, 245, 255, 0.15) 0%, rgba(124, 58, 237, 0.1) 100%);
  border: 1px solid rgba(0, 245, 255, 0.3);
}

.aside-menu .el-menu-item.is-active::before {
  width: 100%;
}

.aside-menu .el-menu-item .el-icon {
  font-size: 20px;
  margin-right: 12px;
}

.sidebar-footer {
  padding: 20px;
  border-top: 1px solid var(--border-color);
}

.system-status {
  display: flex;
  align-items: center;
  justify-content: center;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 20px;
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.status-indicator.online {
  color: #10b981;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #10b981;
  animation: blink 2s ease-in-out infinite;
}

@keyframes blink {
  0%, 100% {
    opacity: 1;
    box-shadow: 0 0 10px rgba(16, 185, 129, 0.6);
  }
  50% {
    opacity: 0.5;
    box-shadow: 0 0 5px rgba(16, 185, 129, 0.3);
  }
}

.status-text {
  font-family: 'Orbitron', sans-serif;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.app-main {
  background: transparent;
  padding: 0;
  overflow-y: auto;
  position: relative;
}

.app-main::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background:
    radial-gradient(ellipse at 20% 30%, rgba(124, 58, 237, 0.08) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 70%, rgba(0, 245, 255, 0.08) 0%, transparent 50%);
  pointer-events: none;
}
</style>
