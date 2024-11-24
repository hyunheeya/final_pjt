<template>
  <div class="container">
    <h2 class="mb-4">내가 좋아요한 상품</h2>

    <!-- 네 가지 기능 버튼 -->
    <div class="mb-4 d-flex flex-wrap gap-2">
      <button 
        @click="currentView = 'deposit'" 
        :class="['btn', currentView === 'deposit' ? 'btn-primary' : 'btn-outline-primary']"
      >
        예금
      </button>
      <button 
        @click="currentView = 'savings'" 
        :class="['btn', currentView === 'savings' ? 'btn-primary' : 'btn-outline-primary']"
      >
        적금
      </button>
      <button 
        @click="currentView = 'depositGraph'" 
        :class="['btn', currentView === 'depositGraph' ? 'btn-success' : 'btn-outline-success']"
      >
        예금 금리 비교하기
      </button>
      <button 
        @click="currentView = 'savingsGraph'" 
        :class="['btn', currentView === 'savingsGraph' ? 'btn-success' : 'btn-outline-success']"
      >
        적금 금리 비교하기
      </button>
    </div>

    <!-- 예금 리스트 -->
    <div v-if="currentView === 'deposit'">
      <div v-if="likedDeposits.length > 0" class="row row-cols-1 row-cols-md-3 g-4">
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
      <p v-else class="text-center text-muted">좋아요한 예금 상품이 없습니다.</p>
    </div>

    <!-- 적금 리스트 -->
    <div v-if="currentView === 'savings'">
      <div v-if="likedSavings.length > 0" class="row row-cols-1 row-cols-md-3 g-4">
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
      <p v-else class="text-center text-muted">좋아요한 적금 상품이 없습니다.</p>
    </div>

    <!-- 예금 금리 비교 -->
    <div v-if="currentView === 'depositGraph'">
      <h3 class="text-center mb-4">예금 금리 비교</h3>
      <canvas id="depositChart" width="400" height="200"></canvas>
    </div>

    <!-- 적금 금리 비교 -->
    <div v-if="currentView === 'savingsGraph'">
      <h3 class="text-center mb-4">적금 금리 비교</h3>
      <canvas id="savingsChart" width="400" height="200"></canvas>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted, nextTick,watch } from 'vue';
import axios from 'axios';
import Chart from 'chart.js/auto';
import useCounterStore from '@/stores/counter';

const store = useCounterStore();
const currentView = ref('deposit'); 
const likedDeposits = ref([]);
const likedSavings = ref([]);
let depositChart = null; // 예금 Chart.js 인스턴스
let savingsChart = null; // 적금 Chart.js 인스턴스

// 좋아요한 상품 데이터 가져오기
const fetchLikedProducts = async () => {
  try {
    const response = await axios.get(`${store.API_URL}/api/accounts/liked-products/`, {
      headers: { Authorization: `Token ${store.token}` },
    });
    likedDeposits.value = response.data.deposits;
    likedSavings.value = response.data.savings;
  } catch (error) {
    console.error('좋아요한 상품 데이터 조회 실패:', error);
  }
};

// currentView 감시
watch(currentView, async (newView) => {
  if (newView === 'depositGraph') {
    await renderDepositChart();
  } else if (newView === 'savingsGraph') {
    await renderSavingsChart();
  }
});

// 예금 금리 비교 그래프
const renderDepositChart = async () => {
  await nextTick(); // DOM이 완전히 렌더링된 뒤 실행
  const labels = likedDeposits.value.map(product => product.fin_prdt_nm);
  const data = likedDeposits.value.map(product => product.intr_rate);

  if (depositChart) {
    depositChart.destroy();
  }

  const ctx = document.getElementById('depositChart').getContext('2d');
  depositChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: '금리 (%)',
          data: data,
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          display: true,
          position: 'top',
        },
      },
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
};

// 적금 금리 비교 그래프
const renderSavingsChart = async () => {
  await nextTick(); // DOM이 완전히 렌더링된 뒤 실행
  const labels = likedSavings.value.map(product => product.fin_prdt_nm);
  const data = likedSavings.value.map(product => product.intr_rate);

  if (savingsChart) {
    savingsChart.destroy();
  }

  const ctx = document.getElementById('savingsChart').getContext('2d');
  savingsChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: '금리 (%)',
          data: data,
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          display: true,
          position: 'top',
        },
      },
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
};

onMounted(fetchLikedProducts);
</script>


<style scoped>
canvas {
  max-width: 100%;
  height: 400px;
}
</style>
