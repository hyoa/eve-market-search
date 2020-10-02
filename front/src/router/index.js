import { createRouter, createWebHashHistory } from 'vue-router'
import List from '../views/List.vue'
import View from '../views/View.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: List
  },
  {
    path: '/list',
    name: 'List',
    component: List
  },
  {
    path: '/filter/:id',
    name: 'View',
    component: View
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
