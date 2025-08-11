import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import MealPlanner from '../views/MealPlanner.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/planner',
    name: 'MealPlanner',
    component: MealPlanner
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
