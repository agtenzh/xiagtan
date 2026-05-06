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
      path: '/brains',
      name: 'Brains',
      component: () => import('@/views/Brains.vue')
    },
    {
      path: '/agents',
      name: 'Agents',
      component: () => import('@/views/Agents.vue')
    },
    {
      path: '/tasks',
      name: 'Tasks',
      component: () => import('@/views/Tasks.vue')
    },
    {
      path: '/monitor',
      name: 'Monitor',
      component: () => import('@/views/Monitor.vue')
    }
  ]
})

export default router
