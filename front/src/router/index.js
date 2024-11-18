import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import ProductsRecommendView from '@/views/ProductsRecommendView.vue'
import ProductsRecommendQuizView from '@/views/ProductsRecommendQuizView.vue'
import ProductsRecommendResultView from '@/views/ProductsRecommendResultView.vue'
import ProductsListView from '@/views/ProductsListView.vue'
import ProductsListDetailView from '@/views/ProductsListDetailView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LoginView from '@/views/LoginView.vue'
import ProfileView from '@/views/ProfileView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/productsrecommend',
      name: 'productsrecommend',
      component: ProductsRecommendView,
    },
    {
      path: '/productsrecommendquiz',
      name: 'productsrecommendquiz',
      component: ProductsRecommendQuizView,
    },
    {
      path: '/productsrecommendresult',
      name: 'productsrecommendresult',
      component: ProductsRecommendResultView,
    },
    {
      path: '/productslist',
      name: 'productslist',
      component: ProductsListView,
    },
    {
      path: '/productslistdetail', // :id 로 바꿔야 함
      name: 'productslistdetail',
      component: ProductsListDetailView,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/profile', // :id 로 바꿔야 함
      name: 'profile',
      component: ProfileView,
    },
  ],
})

export default router
