<template>
  <div class="container">
    <h2 class="mb-4">예금 전체 상품 조회</h2>
    <div v-for="(products, productName) in groupedProducts" :key="productName" class="mb-4">
      <h3>{{ productName }}</h3>
      <div class="row row-cols-1 row-cols-md-3 g-4">
        <div v-for="product in products" :key="product.id" class="col">
          <div class="card h-100">
            <div class="card-body">
              <h5 class="card-title">{{ product.kor_co_nm }}</h5>
              <p class="card-text">
                <strong>저축 기간:</strong> {{ product.save_trm }}개월<br>
                <strong>기본 금리:</strong> {{ product.intr_rate }}%<br>
              </p>
              <RouterLink 
                :to="{ name: 'productsdepositlistdetail', params: { id: product.id } }" 
                class="btn btn-primary"
              >
                상세 정보
              </RouterLink>
              <button 
                @click="toggleLike(product)" 
                :class="product.is_liked ? 'btn-danger' : 'btn-outline-danger'" 
                class="btn"
              >
                ❤️ {{ product.like_count }}
              </button>
            </div>
          </div>
        </div>
      </div>
      <hr>
    </div>
  </div>
</template>

<!-- <script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';

const depositProducts = ref([]);

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

const fetchDepositProducts = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/products/deposit-products/');
    depositProducts.value = response.data;
  } catch (error) {
    console.error('예금 상품을 불러오는 중 오류가 발생했습니다:', error);
  }
};

onMounted(() => {
  fetchDepositProducts();
});
</script> -->

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import useCounterStore from '@/stores/counter';
const store = useCounterStore()

const depositProducts = ref([]); // 예금 상품 리스트

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

// 예금 상품 목록 및 좋아요 상태 가져오기
const fetchDepositProducts = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/products/deposit-products/', {
      headers: { Authorization: `Token ${store.token}` },
    });

    // 상품 목록을 초기화하며 좋아요 상태 기본값 설정
    depositProducts.value = response.data.map(product => ({
      ...product,
      is_liked: false, // 기본값
      like_count: 0,   // 기본값
    }));

    // 각 상품의 좋아요 상태 비동기적으로 가져오기
    const likeDataPromises = depositProducts.value.map(async (product) => {
      const likeResponse = await fetchLikeStatus(product.id);
      product.is_liked = likeResponse.is_liked;
      product.like_count = likeResponse.like_count;
    });

    // 모든 좋아요 데이터 로딩 완료 대기
    await Promise.all(likeDataPromises);
  } catch (error) {
    console.error('예금 상품을 불러오는 중 오류 발생:', error);
  }
};

// 개별 상품의 좋아요 상태 가져오기
const fetchLikeStatus = async (depositId) => {
  try {
    const response = await axios.get(
      `http://localhost:8000/api/products/deposit-products/${depositId}/like-status/`,
      {
        headers: { Authorization: `Token ${store.token}` },
      }
    );
    return response.data; // { is_liked, like_count }
  } catch (error) {
    console.error(`상품 ID ${depositId}의 좋아요 상태를 가져오는 중 오류 발생:`, error);
    return { is_liked: false, like_count: 0 }; // 기본값 반환
  }
};

// 좋아요 상태 토글
const toggleLike = async (product) => {
  try {
    const response = await axios.post(
      `http://localhost:8000/api/products/deposit-products/${product.id}/like/`,
      {},
      {
        headers: { Authorization: `Token ${store.token}` },
      }
    );

    // 좋아요 상태 업데이트
    product.is_liked = response.data.is_liked;
    product.like_count = response.data.like_count;
  } catch (error) {
    console.error('좋아요 상태를 변경하는 중 오류 발생:', error);
  }
};

// 컴포넌트 마운트 시 데이터 로드
onMounted(() => {
  fetchDepositProducts();
});
</script>
