<template>
  <div class="container">
    <h2 class="mb-4">적금 전체 상품 조회</h2>
    <div v-for="(products, productName) in groupedProducts" :key="productName" class="mb-4">
      <h3>{{ productName }}</h3>
      <div class="row row-cols-1 row-cols-md-3 g-4">
        <div v-for="product in products" :key="product.id" class="col">
          <div class="card h-100">
            <div class="card-body">
              <h5 class="card-title">{{ product.kor_co_nm }}</h5>
              <p class="card-text">
                <strong>기본 금리:</strong> {{ product.intr_rate }}%<br>
                <strong>최고 금리:</strong> {{ product.intr_rate2 }}%<br>
                <strong>저축 기간:</strong> {{ product.save_trm }}개월<br>
                <strong>적립 유형:</strong> {{ product.rsrv_type_nm }}
              </p>
              <RouterLink 
                :to="{ name: 'productssavingslistdetail', params: { id: product.id } }" 
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

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';

const savingsProducts = ref([]); // 적금 상품 데이터

// 적금 상품을 그룹화
const groupedProducts = computed(() => {
  const grouped = {};
  savingsProducts.value.forEach(product => {
    if (!grouped[product.fin_prdt_nm]) {
      grouped[product.fin_prdt_nm] = [];
    }
    grouped[product.fin_prdt_nm].push(product);
  });
  return grouped;
});

// 적금 상품 목록 가져오기
const fetchSavingsProducts = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/products/savings-products/', {
      headers: { Authorization: `Token ${localStorage.getItem('token')}` },
    });

    // 상품 목록 초기화 및 기본값 설정
    savingsProducts.value = response.data.map(product => ({
      ...product,
      is_liked: false, // 기본값
      like_count: 0,   // 기본값
    }));

    // 좋아요 상태 가져오기 (비동기 요청)
    const likePromises = savingsProducts.value.map(async (product) => {
      const likeResponse = await fetchLikeStatus(product.id);
      product.is_liked = likeResponse.is_liked;
      product.like_count = likeResponse.like_count;
    });

    await Promise.all(likePromises); // 모든 좋아요 상태 로드 대기
  } catch (error) {
    console.error('적금 상품을 불러오는 중 오류가 발생했습니다:', error);
  }
};

// 좋아요 상태 가져오기
const fetchLikeStatus = async (savingsId) => {
  try {
    const response = await axios.get(
      `http://localhost:8000/api/products/savings-products/${savingsId}/like-status/`,
      {
        headers: { Authorization: `Token ${localStorage.getItem('token')}` },
      }
    );
    return response.data; // { is_liked, like_count }
  } catch (error) {
    console.error(`상품 ID ${savingsId}의 좋아요 상태를 가져오는 중 오류 발생:`, error);
    return { is_liked: false, like_count: 0 }; // 기본값 반환
  }
};

// 좋아요 상태 토글
const toggleLike = async (product) => {
  try {
    const response = await axios.post(
      `http://localhost:8000/api/products/savings-products/${product.id}/like/`,
      {},
      {
        headers: { Authorization: `Token ${localStorage.getItem('token')}` },
      }
    );

    // 응답 데이터로 좋아요 상태와 갯수 업데이트
    product.is_liked = response.data.is_liked;
    product.like_count = response.data.like_count;
  } catch (error) {
    console.error('좋아요 처리 중 오류가 발생했습니다:', error);
  }
};

// 컴포넌트가 로드될 때 데이터 가져오기
onMounted(() => {
  fetchSavingsProducts();
});
</script>

<!-- <script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';

const savingsProducts = ref([]);

const groupedProducts = computed(() => {
  const grouped = {};
  savingsProducts.value.forEach(product => {
    if (!grouped[product.fin_prdt_nm]) {
      grouped[product.fin_prdt_nm] = [];
    }
    grouped[product.fin_prdt_nm].push(product);
  });
  return grouped;
});

const fetchSavingsProducts = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/products/savings-products/');
    savingsProducts.value = response.data;
  } catch (error) {
    console.error('적금 상품을 불러오는 중 오류가 발생했습니다:', error);
  }
};

onMounted(() => {
  fetchSavingsProducts();
});
</script> -->

<style scoped>
.card {
  transition: transform 0.3s;
}

.card:hover {
  transform: translateY(-5px);
}
</style>

<!-- <template>
  <div class="container">
    <h2 class="mb-4">적금 전체 상품 조회</h2>
    <div class="row row-cols-1 row-cols-md-3 g-4">
      <div v-for="product in savingsProducts" :key="product.id" class="col">
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">{{ product.fin_prdt_nm }}</h5>
            <p class="card-text">
              <strong>금융회사:</strong> {{ product.kor_co_nm }}<br>
              <strong>기본 금리:</strong> {{ product.intr_rate }}%<br>
              <strong>저축 기간:</strong> {{ product.save_trm }}개월<br>
              <strong>적립 유형:</strong> {{ product.rsrv_type_nm }}
            </p>
            <RouterLink 
              :to="{ name: 'productssavingslistdetail', params: { id: product.id } }" 
              class="btn btn-primary"
            >
              상세 정보
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const savingsProducts = ref([]);

const fetchSavingsProducts = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/savings-products/');
    savingsProducts.value = response.data;
  } catch (error) {
    console.error('적금 상품을 불러오는 중 오류가 발생했습니다:', error);
  }
};

onMounted(() => {
  fetchSavingsProducts();
});
</script>

<style scoped>
.card {
  transition: transform 0.3s;
}

.card:hover {
  transform: translateY(-5px);
}
</style> -->

<!-- <template>
  <div class="container">
    <h2 class="mb-4">적금 전체 상품 조회</h2>
    <div class="row row-cols-1 row-cols-md-3 g-4">
      <div v-for="product in savingsProducts" :key="product.fin_prdt_nm" class="col">
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">{{ product.fin_prdt_nm }}</h5>
            <p class="card-text">
              <strong>금융회사:</strong> {{ product.kor_co_nm }}<br>
              <strong>기본 금리:</strong> {{ product.min_intr_rate }}% ~ {{ product.max_intr_rate }}%<br>
              <strong>저축 기간:</strong> {{ product.min_save_trm }}개월 ~ {{ product.max_save_trm }}개월
            </p>
            <RouterLink 
              :to="{ 
                name: 'productssavingslistdetail', 
                params: { 
                  fin_prdt_nm: product.fin_prdt_nm,
                  rsrv_type_nm: product.rsrv_type_nm 
                } 
              }" 
              class="btn btn-primary"
            >
              상세 정보
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const savingsProducts = ref([]);

const fetchSavingsProducts = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/savings-products/');
    savingsProducts.value = response.data;
  } catch (error) {
    console.error('적금 상품을 불러오는 중 오류가 발생했습니다:', error);
  }
};

onMounted(() => {
  fetchSavingsProducts();
});
</script> -->