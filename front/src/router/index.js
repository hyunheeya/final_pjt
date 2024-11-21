import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import ProductsRecommendView from '@/views/ProductsRecommendView.vue'
import ProductsRecommendQuizView from '@/views/ProductsRecommendQuizView.vue'
import ProductsRecommendResultView from '@/views/ProductsRecommendResultView.vue'
import ProductsListView from '@/views/ProductsListView.vue'
// import ProductsDepositListView from '@/components/ProductsDepositListView.vue'
// import ProductsSavingsListView from '@/components/ProductsSavingsListView.vue'
import ProductsDepositListDetailView from '@/views/ProductsDepositListDetailView.vue'
import ProductsSavingsListDetailView from '@/views/ProductsSavingsListDetailView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LoginView from '@/views/LoginView.vue'
import ProfileView from '@/views/ProfileView.vue'
import useCounterStore from '@/stores/counter.js'

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
      beforeEnter: (to, from) => {
        if (!useCounterStore.isLogin) {
          console.log('로그인이 필요합니다.');
          return { name: 'login' };
        }
      }
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
      props: (route) => ({
        results: route.query.results ? JSON.parse(route.query.results) : [],
      }),
    },
    {
      path: '/productslist',
      name: 'productslist',
      component: ProductsListView,
      beforeEnter: (to, from) => {
        if (!useCounterStore.isLogin) {
          console.log('로그인이 필요합니다.');
          return { name: 'login' };
        }
      }
    },
    // 부모-자식 컴포넌트 구조라서 라우터 필요없음
    // {
    //   path: '/productsdepositlist',
    //   name: 'productsdepositlist',
    //   component: ProductsDepositListView,
    // },
    // {
    //   path: '/productssavingslist',
    //   name: 'productssavingslist',
    //   component: ProductsSavingsListView,
    // },
    {
      path: '/productsdepositlistdetail/:fin_prdt_nm',  // 파라미터 : 상품명(fin_prdt_nm)
      name: 'productsdepositlistdetail',
      component: ProductsDepositListDetailView,
    },
    {
      path: '/productssavingslistdetail/:fin_prdt_nm/:rsrv_type_nm', // 파라미터:상품명(fin_prdt_nm)과 적립방식(rsrv_type_nm)
      name: 'productssavingslistdetail',
      component: ProductsSavingsListDetailView,
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
      path: '/profile',
      name: 'profile',
      component: ProfileView,
    },
  ],
})

export default router
