import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('@/views/Home.vue')
    },
    {
      path: '/agents',
      name: 'Agents',
      component: () => import('@/views/Agents.vue')
    },
    {
      path: '/models',
      name: 'Models',
      component: () => import('@/views/Models.vue')
    },
    {
      path: '/tasks',
      name: 'Tasks',
      component: () => import('@/views/Tasks.vue')
    },
    {
      path: '/logs',
      name: 'Logs',
      component: () => import('@/views/Logs.vue')
    },
    {
      path: '/config',
      name: 'Config',
      component: () => import('@/views/Config.vue')
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: () => import('@/views/MindMap.vue')
    },
    {
      path: '/monitor',
      name: 'Monitor',
      component: () => import('@/views/Dashboard.vue')
    },
    {
      path: '/settings',
      name: 'Settings',
      component: () => import('@/views/Settings.vue')
    }
  ]
})

export default router
