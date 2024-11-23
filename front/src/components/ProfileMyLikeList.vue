<template>
  <div class="container">
    <h2 class="mb-4">내가 좋아요한 상품</h2>
    <div class="mb-4">
      <button 
        @click="currentView = 'deposit'" 
        :class="['btn', 'me-2', currentView === 'deposit' ? 'btn-primary' : 'btn-outline-primary']"
      >
        예금
      </button>
      <button 
        @click="currentView = 'savings'"
        :class="['btn', 'me-2', currentView === 'savings' ? 'btn-primary' : 'btn-outline-primary']"
      >
        적금
      </button>
    </div>

    <!-- 예금 좋아요 목록 -->
    <div v-if="currentView === 'deposit'" class="row row-cols-1 row-cols-md-3 g-4">
      <div v-for="product in likedDeposits" :key="product.id" class="col">
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">{{ product.fin_prdt_nm }}</h5>
            <p class="text-muted small">{{ product.kor_co_nm }}</p>
            <p class="card-text">
              <strong>저축 기간:</strong> {{ product.save_trm }}개월<br>
              <strong>기본 금리:</strong> {{ product.intr_rate }}%
            </p>
            <div class="d-flex justify-content-between align-items-center">
              <RouterLink 
                :to="{ name: 'productsdepositlistdetail', params: { id: product.id } }" 
                class="btn btn-primary"
              >
                상세 정보
              </RouterLink>
              <span class="text-danger">❤️ {{ product.like_count }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 적금 좋아요 목록 -->
    <div v-if="currentView === 'savings'" class="row row-cols-1 row-cols-md-3 g-4">
      <div v-for="product in likedSavings" :key="product.id" class="col">
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">{{ product.fin_prdt_nm }}</h5>
            <p class="text-muted small">{{ product.kor_co_nm }}</p>
            <p class="card-text">
              <strong>저축 기간:</strong> {{ product.save_trm }}개월<br>
              <strong>기본 금리:</strong> {{ product.intr_rate }}%
            </p>
            <div class="d-flex justify-content-between align-items-center">
              <RouterLink 
                :to="{ name: 'productssavingslistdetail', params: { id: product.id } }" 
                class="btn btn-primary"
              >
                상세 정보
              </RouterLink>
              <span class="text-danger">❤️ {{ product.like_count }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import useCounterStore from '@/stores/counter';

const store = useCounterStore();
const currentView = ref('deposit');
const likedDeposits = ref([]);
const likedSavings = ref([]);

// 예금 좋아요 목록 가져오기
const fetchLikedDeposits = async () => {
  try {
    const response = await axios.get(`${store.API_URL}/api/accounts/liked-products/`, {
      headers: { Authorization: `Token ${store.token}` }
    });
    likedDeposits.value = response.data.deposits;
  } catch (error) {
    console.error('예금 좋아요 목록 조회 실패:', error);
  }
};

// 적금 좋아요 목록 가져오기
const fetchLikedSavings = async () => {
  try {
    const response = await axios.get(`${store.API_URL}/api/accounts/liked-products/`, {
      headers: { Authorization: `Token ${store.token}` }
    });
    likedSavings.value = response.data.savings;
  } catch (error) {
    console.error('적금 좋아요 목록 조회 실패:', error);
  }
};

onMounted(() => {
  fetchLikedDeposits();
  fetchLikedSavings();
});
</script>