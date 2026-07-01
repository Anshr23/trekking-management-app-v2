import { createRouter, createWebHistory } from 'vue-router'

import LoginView from '../views/auth/LoginView.vue'
import RegisterView from '../views/auth/RegisterView.vue'

import AdminDashboard from '../views/admin/AdminDashboard.vue'
import StaffDashboard from '../views/staff/StaffDashboard.vue'
import TrekkerDashboard from '../views/trekker/TrekkerDashboard.vue'


const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: {
      guestOnly: true
    }
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
    meta: {
      guestOnly: true
    }
  },
  {
    path: '/admin/dashboard',
    name: 'admin-dashboard',
    component: AdminDashboard,
    meta: {
      requiresAuth: true,
      role: 'admin'
    }
  },
  {
    path: '/staff/dashboard',
    name: 'staff-dashboard',
    component: StaffDashboard,
    meta: {
      requiresAuth: true,
      role: 'staff'
    }
  },
  {
    path: '/trekker/dashboard',
    name: 'trekker-dashboard',
    component: TrekkerDashboard,
    meta: {
      requiresAuth: true,
      role: 'trekker'
    }
  }
]


const router = createRouter({
  history: createWebHistory(),
  routes
})


router.beforeEach((to) => {
  const token = localStorage.getItem('access_token')
  const savedUser = localStorage.getItem('user')

  let user = null

  if (savedUser) {
    try {
      user = JSON.parse(savedUser)
    } catch {
      localStorage.removeItem('user')
      localStorage.removeItem('access_token')
    }
  }

  if (to.meta.requiresAuth && (!token || !user)) {
    return '/login'
  }

  if (
    to.meta.requiresAuth &&
    to.meta.role &&
    user.role !== to.meta.role
  ) {
    if (user.role === 'admin') {
      return '/admin/dashboard'
    }

    if (user.role === 'staff') {
      return '/staff/dashboard'
    }

    return '/trekker/dashboard'
  }

  if (to.meta.guestOnly && token && user) {
    if (user.role === 'admin') {
      return '/admin/dashboard'
    }

    if (user.role === 'staff') {
      return '/staff/dashboard'
    }

    return '/trekker/dashboard'
  }
})


export default router