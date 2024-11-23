<!-- <template>
  <div class="container">
    <h2 class="mb-4">예금 상품 조회</h2>
    <div class="mb-4">
      <button @click="fetchAllDeposits" class="btn btn-primary">전체 보기</button>
      <button @click="fetchDepositsByInterest" class="btn btn-secondary">금리순 보기</button>
    </div>
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
</template> -->
<!-- <template>
  <div class="container">
    <h2 class="mb-4">예금 상품 조회</h2>
    <div class="mb-4">
      <button @click="fetchAllDeposits" class="btn btn-primary">전체 보기</button>
      <button @click="fetchDepositsByInterest" class="btn btn-secondary">금리순 보기</button>
    </div>
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
      <hr />
    </div>
  </div>
</template> -->

<template>
  <div class="container">
    <h2 class="mb-4">예금 상품 조회</h2>
    <div class="mb-4">
      <button @click="showAllDeposits" class="btn btn-primary">전체 보기</button>
      <button @click="showDepositsByRate" class="btn btn-secondary">금리순 보기</button>
    </div>
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
              <div class="d-flex justify-content-between">
                <RouterLink 
                  :to="{ name: 'productsdepositlistdetail', params: { id: product.id } }" 
                  class="btn btn-primary"
                >
                  상세 정보
                </RouterLink>
                <button 
                  @click="toggleLike(product)" 
                  :class="['btn', product.is_liked ? 'btn-danger' : 'btn-outline-danger']"
                >
                  <span class="heart-icon">❤️</span> 
                  <span class="like-count">{{ product.like_count }}</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <hr />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import useCounterStore from '@/stores/counter';

const store = useCounterStore();
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

// 전체 보기 API 호출
const fetchAllDeposits = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/products/deposit-products/', {
      headers: { Authorization: `Token ${store.token}` },
    });

    // 전체 데이터를 상태에 저장
    depositProducts.value = response.data.map(product => ({
      ...product,
      is_liked: false, // 좋아요 기본값
      like_count: 0,   // 좋아요 기본값
    }));

    // 좋아요 상태 가져오기
    await loadLikeStatuses();
  } catch (error) {
    console.error('전체 데이터를 가져오는 중 오류 발생:', error);
  }
};

/// 예금 상품 데이터 가져오기
const fetchDeposits = async (sortType = 'default') => {
  try {
    const response = await axios.get(`http://localhost:8000/api/products/deposit-products/`, {
      params: { sort: sortType },
      headers: { 
        Authorization: `Token ${store.token}` 
      }
    });
    
    depositProducts.value = response.data;
  } catch (error) {
    console.error('데이터를 가져오는 중 오류 발생:', error);
  }
};

// 전체순 보기
const showAllDeposits = () => {
  fetchDeposits('default');
};

// 금리순 보기
const showDepositsByRate = () => {
  fetchDeposits('rate');
};

// 좋아요 상태 가져오기
const loadLikeStatuses = async () => {
  const likeDataPromises = depositProducts.value.map(async (product) => {
    const likeResponse = await fetchLikeStatus(product.id);
    product.is_liked = likeResponse.is_liked;
    product.like_count = likeResponse.like_count;
  });

  await Promise.all(likeDataPromises); // 모든 좋아요 데이터 로딩 대기
};

// 좋아요 상태 API 호출
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
    console.error(`좋아요 상태를 가져오는 중 오류 발생: ${error}`);
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

    product.is_liked = response.data.is_liked;
    product.like_count = response.data.like_count;
  } catch (error) {
    console.error('좋아요 상태 변경 중 오류 발생:', error);
  }
};

// 컴포넌트가 로드될 때 전체 보기 데이터 가져오기
onMounted(() => {
  fetchAllDeposits();
});
</script>
