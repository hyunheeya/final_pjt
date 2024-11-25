<template>
  <div class="container">
    <h2 class="mb-4">예금 상품 조회</h2>
    <div class="mb-4">
      <button 
        @click="showAllDeposits" 
        :class="['btn', activeButton === 'all' ? 'btn-primary' : 'btn-outline-primary']"
        class="me-2"
      >
        전체
      </button>
      <button 
        @click="showDepositsByRate" 
        :class="['btn', activeButton === 'rate' ? 'btn-primary' : 'btn-outline-primary']"
        class="me-2"
      >
        금리순
      </button>
      <button 
        @click="showDepositsByLikes" 
        :class="['btn', activeButton === 'likes' ? 'btn-primary' : 'btn-outline-primary']"
        class="me-2"
      >
        좋아요순
      </button>
      <button 
        @click="showDepositsByBank" 
        :class="['btn', activeButton === 'bank' ? 'btn-primary' : 'btn-outline-primary']"
        class="me-2"
      >
        은행명순
      </button>
    </div>

    <div v-for="(products, productName) in groupedProducts" :key="productName" class="mb-4">
      <h3 class="mb-3">{{ productName }}</h3>
      <div class="row row-cols-1 row-cols-md-3 g-4">
        <div v-for="product in products" :key="product.id" class="col"> 
          <div class="card h-100">
            <div class="card-header position-relative p-3 bg-light">
              <img 
                :src="getImageUrl(product.kor_co_nm)"
                :alt="product.kor_co_nm"
                class="bank-logo img-fluid"
              />
              <h6 class="text-center mt-2 mb-0">{{ product.fin_prdt_nm }}</h6>
            </div>
            <div class="card-body">
              <p class="text-muted small mb-3 text-center">{{ product.kor_co_nm }}</p>
              <p class="card-text">
                <strong>저축 기간:</strong> {{ product.save_trm }}개월<br>
                <strong>기본 금리:</strong> {{ product.intr_rate }}%
              </p>
                <div class="d-flex justify-content-between align-items-center mt-3">
                  <RouterLink 
                    :to="{ name: 'productsdepositlistdetail', params: { id: product.id } }" 
                    class="btn btn-primary"
                  >
                    상세 정보
                  </RouterLink>
                  <button 
                    @click="toggleLike(product)" 
                    :class="['btn', 'btn-sm', product.is_liked ? 'btn-danger' : 'btn-outline-danger']"
                  >
                    <span class="heart-icon">❤️</span>
                  <span class="ms-1">{{ product.like_count }}</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <hr class="mt-4" />
    </div>
  </div>
</template>



<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import useCounterStore from '@/stores/counter';

const store = useCounterStore();
const depositProducts = ref([]); // 예금 상품 리스트

// 이미지 동적 로딩을 위한 설정
const getImageUrl = (bankName) => {
  try {
    return new URL(`../assets/bank_logo/${bankName}.png`, import.meta.url).href;
  } catch (error) {
    console.error(`은행 로고 로딩 실패: ${bankName}`, error);
    return ''; // 기본 이미지 경로 또는 빈 문자열 반환
  }
};

// 그룹화된 상품 데이터 계산
const groupedProducts = computed(() => {
  const grouped = {};
  depositProducts.value.forEach(product => {
    if (!grouped[product.fin_prdt_nm]) {
      grouped[product.fin_prdt_nm] = [];
    }
    grouped[product.fin_prdt_nm].push(product);
  });
  return grouped;
});

// 예금 상품 데이터 가져오기 (단일 API 호출)
const fetchDeposits = async (sortType = 'default') => {
  try {
    const response = await axios.get(`${store.API_URL}/api/products/deposit-products/`, {
      params: { sort: sortType },
      headers: { Authorization: `Token ${store.token}` }
    });
    depositProducts.value = response.data;
  } catch (error) {
    console.error('데이터를 불러오는 중 오류가 발생했습니다:', error);
  }
};

// 현재 활성화된 버튼 상태 관리
const activeButton = ref('all'); // 초기값은 '전체'

// 전체보기
const showAllDeposits = () => {
  fetchDeposits('default');
  activeButton.value = 'all'; // '전체' 버튼 활성화
};

// 금리순 보기
const showDepositsByRate = () => {
  fetchDeposits('rate');
  activeButton.value = 'rate'; // '금리순' 버튼 활성화
};

// 좋아요순 보기 함수 추가
const showDepositsByLikes = () => {
  fetchDeposits('likes');
  activeButton.value = 'likes'; // '은행명순' 버튼 활성화

};

// 은행명순 보기
const showDepositsByBank = () => {
  fetchDeposits('bank');
  activeButton.value = 'bank'; // '좋아요순' 버튼 활성화
};


// 좋아요 상태 토글
const toggleLike = async (product) => {
  try {
    const response = await axios.post(
      `${store.API_URL}/api/products/deposit-products/${product.id}/like/`,
      {},
      {
        headers: { Authorization: `Token ${store.token}` },
      }
    );
    product.is_liked = response.data.is_liked;
    product.like_count = response.data.like_count;
  } catch (error) {
    console.error('좋아요 상태 변경 중 오류가 발생했습니다:', error);
  }
};

// 컴포넌트가 로드될 때 전체 보기 데이터 가져오기
onMounted(() => {
  fetchDeposits();
});
</script>

<style scoped>
  .bank-logo {
    max-height: 50px;
    display: block;
    margin: 0 auto;
    object-fit: contain;
  }

  .card-header {
    background-color: #f8f9fa;
    border-bottom: 1px solid rgba(0,0,0,.125);
  }
</style>