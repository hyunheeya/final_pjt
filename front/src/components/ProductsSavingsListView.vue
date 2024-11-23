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

    <!-- 금리순/전체순 버튼 -->
    <div class="mb-4">
      <button @click="fetchAllSavings" :class="currentSortType === 'all' ? 'btn-primary' : 'btn-secondary'">
        전체 보기
      </button>
      <button @click="fetchSavingsByInterest" :class="currentSortType === 'interest' ? 'btn-primary' : 'btn-secondary'">
        금리순 보기
      </button>
    </div>

    <!-- 적금 상품 리스트 -->
    <div v-if="savingsProducts.length > 0">
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
                <RouterLink 
                :to="{ name: 'productssavingslistdetail', params: { id: product.id } }" 
                class="btn btn-primary"
              >
                상세 정보
              </RouterLink>
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
      </div>
    </div>
    <div v-else>
      <p>적금 데이터를 불러오는 중입니다...</p>
    </div>

    <!-- 페이지네이션 컨트롤 -->
    <div class="pagination-controls">
      <button @click="goToPreviousPage" :disabled="currentPage === 1" class="btn btn-secondary">
        이전
      </button>
      <span>페이지 {{ currentPage }} / {{ totalPages }}</span>
      <button @click="goToNextPage" :disabled="currentPage === totalPages" class="btn btn-secondary">
        다음
      </button>
    </div>
  </div>
</template>


<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import useCounterStore from '@/stores/counter';

const store = useCounterStore();
const savingsProducts = ref([]); // 적금 상품 리스트

// 페이지네이션 관련 변수
const currentSortType = ref('all'); // 'all' = 전체순, 'interest' = 금리순
const currentPage = ref(1);         // 현재 페이지
const totalPages = ref(0);          // 전체 페이지 수
const perPage = 10;                 // 한 페이지당 출력할 항목 수


// 그룹화된 상품 데이터 계산
const groupedSavingsProducts = computed(() => {
  const grouped = {};
  // savingsProducts가 배열인지 확인
  if (Array.isArray(savingsProducts.value)) {
    savingsProducts.value.forEach(product => {
      if (!grouped[product.fin_prdt_nm]) {
        grouped[product.fin_prdt_nm] = [];
      }
      grouped[product.fin_prdt_nm].push(product);
    });
  }
  return grouped;
});


const fetchAllSavings = async () => {
  currentSortType.value = 'all'; // 전체순으로 설정
  currentPage.value = 1;         // 페이지 초기화
  await fetchPaginatedSavings(); // 전체순 데이터 로드
};

const fetchSavingsByInterest = async () => {
  currentSortType.value = 'interest'; // 금리순으로 설정
  currentPage.value = 1;              // 페이지 초기화
  await fetchPaginatedSavings();      // 금리순 데이터 로드
};

// // 적금 전체 보기 API 호출
// const fetchAllSavings = async () => {
//   try {
//     const response = await axios.get('http://localhost:8000/api/products/savings-products/sorted/', {
//       headers: { Authorization: `Token ${store.token}` },
//     });

//     // 전체 적금 데이터를 상태에 저장
//     savingsProducts.value = response.data.map(product => ({
//       ...product,
//       is_liked: false, // 좋아요 기본값
//       like_count: 0,   // 좋아요 기본값
//     }));

//     // 좋아요 상태 가져오기
//     await loadSavingsLikeStatuses();
//   } catch (error) {
//     console.error('전체 적금 데이터를 가져오는 중 오류 발생:', error);
//   }
// };

// // 적금 금리순 보기 API 호출
// const fetchSavingsByInterest = async () => {
//   try {
//     const response = await axios.get('http://localhost:8000/api/products/savings-products/sorted/', {
//       headers: { Authorization: `Token ${store.token}` },
//     });

//     // 금리순 데이터를 상태에 저장
//     savingsProducts.value = response.data.map(product => ({
//       ...product,
//       is_liked: false, // 좋아요 기본값
//       like_count: 0,   // 좋아요 기본값
//     }));

//     // 좋아요 상태 가져오기
//     await loadSavingsLikeStatuses();
//   } catch (error) {
//     console.error('금리순 적금 데이터를 가져오는 중 오류 발생:', error);
//   }
// };

// 페이지네이션
const fetchPaginatedSavings = async (page = 1) => {
  try {
    const url =
      currentSortType.value === 'all'
        ? 'http://localhost:8000/api/products/savings-products/' // 전체순 API
        : 'http://localhost:8000/api/products/savings-products/sorted/'; // 금리순 API

    const response = await axios.get(url, {
      params: { page, per_page: perPage }, // 페이지 번호와 한 페이지당 항목 수 전달
      headers: { Authorization: `Token ${store.token}` },
    });

    // 응답 데이터가 배열인지 확인하고 저장
    if (Array.isArray(response.data)) {
      // 배열 데이터 처리
      savingsProducts.value = response.data; // API가 배열 형식 데이터를 반환하는 경우
      currentPage.value = page;             // 현재 페이지를 설정
      totalPages.value = Math.ceil(response.data.length / perPage); // 페이지 수 계산 (더미로 설정)
    } else if (response.data.results && Array.isArray(response.data.results)) {
      // results 키가 포함된 경우 처리
      savingsProducts.value = response.data.results;
      currentPage.value = response.data.page;
      totalPages.value = response.data.total_pages;
    } else {
      console.error('API 응답이 예상한 구조가 아닙니다:', response.data);
      savingsProducts.value = []; // 기본값으로 빈 배열 설정
    }
  } catch (error) {
    console.error('페이지네이션 데이터를 가져오는 중 오류 발생:', error);
    savingsProducts.value = []; // 오류 발생 시 빈 배열로 초기화
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
  savingsProducts.value = []; // 초기 상태를 빈 배열로 설정
  fetchAllSavings();
  loadSavingsLikeStatuses();
});
</script>


<!-- <script setup>
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
</script> -->

<style scoped>
.card {
  transition: transform 0.3s;
}

.card:hover {
  transform: translateY(-5px);
}
</style>
