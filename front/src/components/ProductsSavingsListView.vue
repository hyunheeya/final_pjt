<!-- <template>
  <div class="container">
    <h2 class="mb-4">적금 상품 조회</h2>
    <div class="mb-4">
      <button @click="fetchAllSavings" class="btn btn-primary">전체 보기</button>
      <button @click="fetchSavingsByInterest" class="btn btn-secondary">금리순 보기</button>
    </div>
    <div v-for="(products, productName) in groupedSavingsProducts" :key="productName" class="mb-4">
      <h3>{{ productName }}</h3>
      <div class="row row-cols-1 row-cols-md-3 g-4">
        <div v-for="product in products" :key="product.id" class="col">
          <div class="card h-100">
            <div class="card-body">
              <h5 class="card-title">{{ product.kor_co_nm }}</h5>
              <p class="card-text">
                <strong>저축 기간:</strong> {{ product.save_trm }}개월<br>
                <strong>금리:</strong> {{ product.intr_rate }}%<br>
                <strong>적금 종류:</strong> {{ product.rsrv_type_nm }}<br>
              </p>
              <button 
                @click="toggleSavingsLike(product)" 
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
    <h2 class="mb-4">적금 상품 조회</h2>
    <div class="mb-4">
      <button @click="fetchSavings('default')" class="btn btn-primary me-2">전체 보기</button>
      <button @click="fetchSavings('rate')" class="btn btn-secondary">금리순 보기</button>
    </div>
    <div v-for="(products, productName) in groupedProducts" :key="productName" class="mb-4">
      <h3 class="mb-3">{{ productName }}</h3>
      <div class="row row-cols-1 row-cols-md-3 g-4">
        <div v-for="product in products" :key="product.id" class="col">
          <div class="card h-100">
            <div class="card-body">
              <h5 class="card-title">{{ product.kor_co_nm }}</h5>
              <p class="card-text">
                <strong>저축 기간:</strong> {{ product.save_trm }}개월<br>
                <strong>기본 금리:</strong> {{ product.intr_rate }}%<br>
                <strong>적금 종류:</strong> {{ product.rsrv_type_nm }}<br>
              </p>
              <div class="d-flex justify-content-between align-items-center mt-3">
                <RouterLink 
                  :to="{ name: 'productssavingslistdetail', params: { id: product.id } }" 
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



<!-- <script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import useCounterStore from '@/stores/counter';

const store = useCounterStore();
const savingsProducts = ref([]); // 적금 상품 리스트

// 그룹화된 상품 데이터 계산
const groupedSavingsProducts = computed(() => {
  const grouped = {};
  savingsProducts.value.forEach(product => {
    if (!grouped[product.fin_prdt_nm]) {
      grouped[product.fin_prdt_nm] = [];
    }
    grouped[product.fin_prdt_nm].push(product);
  });
  return grouped;
});

// 적금 전체 보기 API 호출
const fetchAllSavings = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/products/savings-products/sorted/', {
      headers: { Authorization: `Token ${store.token}` },
    });

    // 전체 적금 데이터를 상태에 저장
    savingsProducts.value = response.data.map(product => ({
      ...product,
      is_liked: false, // 좋아요 기본값
      like_count: 0,   // 좋아요 기본값
    }));

    // 좋아요 상태 가져오기
    await loadSavingsLikeStatuses();
  } catch (error) {
    console.error('전체 적금 데이터를 가져오는 중 오류 발생:', error);
  }
};

// 적금 금리순 보기 API 호출
const fetchSavingsByInterest = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/products/savings-products/sorted/', {
      headers: { Authorization: `Token ${store.token}` },
    });

    // 금리순 데이터를 상태에 저장
    savingsProducts.value = response.data.map(product => ({
      ...product,
      is_liked: false, // 좋아요 기본값
      like_count: 0,   // 좋아요 기본값
    }));

    // 좋아요 상태 가져오기
    await loadSavingsLikeStatuses();
  } catch (error) {
    console.error('금리순 적금 데이터를 가져오는 중 오류 발생:', error);
  }
};

// 적금 좋아요 상태 가져오기
const loadSavingsLikeStatuses = async () => {
  const likeDataPromises = savingsProducts.value.map(async (product) => {
    const likeResponse = await fetchSavingsLikeStatus(product.id);
    product.is_liked = likeResponse.is_liked;
    product.like_count = likeResponse.like_count;
  });

  await Promise.all(likeDataPromises); // 모든 좋아요 데이터 로딩 대기
};

// 적금 개별 좋아요 상태 가져오기
const fetchSavingsLikeStatus = async (savingsId) => {
  try {
    const response = await axios.get(
      `http://localhost:8000/api/products/savings-products/${savingsId}/like-status/`,
      {
        headers: { Authorization: `Token ${store.token}` },
      }
    );
    return response.data; // { is_liked, like_count }
  } catch (error) {
    console.error(`적금 ID ${savingsId}의 좋아요 상태를 가져오는 중 오류 발생:`, error);
    return { is_liked: false, like_count: 0 }; // 기본값 반환
  }
};

// 적금 좋아요 상태 토글
const toggleSavingsLike = async (product) => {
  try {
    const response = await axios.post(
      `http://localhost:8000/api/products/savings-products/${product.id}/like/`,
      {},
      {
        headers: { Authorization: `Token ${store.token}` },
      }
    );

    // 좋아요 상태 업데이트
    product.is_liked = response.data.is_liked;
    product.like_count = response.data.like_count;
  } catch (error) {
    console.error('적금 좋아요 상태를 변경하는 중 오류 발생:', error);
  }
};

// 컴포넌트 마운트 시 기본적으로 전체 적금 데이터 로드
onMounted(() => {
  fetchAllSavings();
});
</script> -->


<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import useCounterStore from '@/stores/counter';

const store = useCounterStore();
const savingsProducts = ref([]); // 적금 상품 리스트

// 그룹화된 상품 데이터 계산
// 한 상품 모여서 보이게 하기
const groupedProducts = computed(() => {
  const grouped = {};
  savingsProducts.value.forEach(product => {  // 여기를 savingsProducts로 수정
    if (!grouped[product.fin_prdt_nm]) {
      grouped[product.fin_prdt_nm] = [];
    }
    grouped[product.fin_prdt_nm].push(product);
  });
  return grouped;
});

// 적금 상품 데이터 가져오기 (단일 API 호출)
const fetchSavings = async (sortType = 'default') => {
  try {
    const response = await axios.get(`${store.API_URL}/api/products/savings-products/`, {
      params: { sort: sortType },
      headers: { Authorization: `Token ${store.token}` }
    });
    savingsProducts.value = response.data;
  } catch (error) {
    console.error('데이터를 불러오는 중 오류가 발생했습니다:', error);
  }
};

// 좋아요 상태 토글
const toggleLike = async (product) => {
  try {
    const response = await axios.post(
      `${store.API_URL}/api/products/savings-products/${product.id}/like/`,
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
  fetchSavings();
});
</script>


<style scoped>
.card {
  transition: transform 0.3s;
}

.card:hover {
  transform: translateY(-5px);
}
</style>
