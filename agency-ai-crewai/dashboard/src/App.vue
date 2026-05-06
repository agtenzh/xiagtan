<template>
  <el-config-provider :locale="zhCn">
    <div class="app-container">
      <!-- 侧边栏 -->
      <el-aside width="220px" class="app-aside">
        <div class="logo">
          <h2>AI代理系统</h2>
          <span class="version">CrewAI v2.0</span>
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
          <el-menu-item index="/brains">
            <el-icon><Cpu /></el-icon>
            <span>大脑管理</span>
          </el-menu-item>
          <el-menu-item index="/agents">
            <el-icon><User /></el-icon>
            <span>代理管理</span>
          </el-menu-item>
          <el-menu-item index="/tasks">
            <el-icon><List /></el-icon>
            <span>任务管理</span>
          </el-menu-item>
          <el-menu-item index="/monitor">
            <el-icon><DataLine /></el-icon>
            <span>系统监控</span>
          </el-menu-item>
        </el-menu>
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
  Cpu,
  User,
  List,
  DataLine
} from '@element-plus/icons-vue'

const route = useRoute()
const currentRoute = computed(() => route.path)
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB',
    'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}

.app-container {
  display: flex;
  height: 100vh;
}

.app-aside {
  background-color: #1e293b;
  overflow-y: auto;
}

.logo {
  height: 80px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #fff;
  border-bottom: 1px solid #334155;
}

.logo h2 {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.logo .version {
  font-size: 11px;
  color: #94a3b8;
  margin-top: 4px;
}

.aside-menu {
  border-right: none;
  background-color: #1e293b;
}

.aside-menu .el-menu-item {
  color: #94a3b8;
  height: 48px;
  line-height: 48px;
}

.aside-menu .el-menu-item:hover {
  background-color: #334155;
  color: #fff;
}

.aside-menu .el-menu-item.is-active {
  color: #3b82f6;
  background-color: #1e3a5f;
}

.app-main {
  background-color: #f1f5f9;
  padding: 20px;
  overflow-y: auto;
}
</style>
