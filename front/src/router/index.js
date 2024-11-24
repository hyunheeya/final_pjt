import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import ProductsRecommendView from '@/views/ProductsRecommendView.vue'
import ProductsRecommendQuizView from '@/views/ProductsRecommendQuizView.vue'
import ProductsRecommendResultView from '@/views/ProductsRecommendResultView.vue'
import ProductsListView from '@/views/ProductsListView.vue'
import ProductsDepositListView from '@/components/ProductsDepositListView.vue'
import ProductsSavingsListView from '@/components/ProductsSavingsListView.vue'
import ProductsDepositListDetailView from '@/views/ProductsDepositListDetailView.vue'
import ProductsSavingsListDetailView from '@/views/ProductsSavingsListDetailView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LoginView from '@/views/LoginView.vue'
import ProfileView from '@/views/ProfileView.vue'
import BankMapView from '@/views/BankMapView.vue'
import BoardView from '@/views/BoardView.vue'
import CreateView from '@/views/CreateView.vue'
import BoardArticleListView from '@/views/BoardArticleListView.vue'
import BoardArticleDetailView from '@/views/BoardArticleDetailView.vue'
import BoardArticleEditView from '@/views/BoardArticleEditView.vue'
import ExchangesView from '@/views/ExchangesView.vue'
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
        const counterStore = useCounterStore() // 스토어 인스턴스 가져오기
        if (!counterStore.isLogin) {
          console.log(counterStore.isLogin)
          console.log('로그인이 필요합니다.')
          return { name: 'login' }
        }}
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
      children: [
        {
          path: 'deposit', // 부모 경로를 기준으로 함
          name: 'ProductsDepositListView',
          component: ProductsDepositListView, // 자식 컴포넌트
        },
        {
          path: '/productssavingslist',
          name: 'productssavingslist',
          component: ProductsSavingsListView,
        },
      ],
      beforeEnter: (to, from) => {
        const counterStore = useCounterStore() // 스토어 인스턴스 가져오기
        if (!counterStore.isLogin) {
          console.log(counterStore.isLogin)
          console.log('로그인이 필요합니다.')
          return { name: 'login' }
        }}
    },
    {
      path: '/productsdepositlistdetail/:id',  // 파라미터 : 상품명(fin_prdt_nm)
      name: 'productsdepositlistdetail',
      component: ProductsDepositListDetailView,
    },
    {
      path: '/productssavingslistdetail/:id', // 파라미터:상품명(fin_prdt_nm)과 적립방식(rsrv_type_nm)
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
      path: '/bankmap',
      name: 'bankmap',
      component: BankMapView,
    },
    {
      path: '/board',
      name: 'board',
      component: BoardView,
      beforeEnter: (to, from) => {
        const counterStore = useCounterStore() // 스토어 인스턴스 가져오기
        if (!counterStore.isLogin) {
          console.log(counterStore.isLogin)
          console.log('로그인이 필요합니다.')
          return { name: 'login' }
        }}
    },
    {
      path: '/create',
      name: 'create',
      component: CreateView,
    },
    {
      path: '/board/articles',
      name: 'boardarticlelist',
      component: BoardArticleListView,
    },
    {
      path: '/board/articles/:id',
      name: 'boardarticledetail',
      component: BoardArticleDetailView,
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
    },
    {
      path: '/board/articles/:id/edit',
      name: 'edit',
      component: BoardArticleEditView,
    },
    {
      path: '/exchanges',
      name: 'exchanges',
      component: ExchangesView,
    },
  ],
})

export default router
