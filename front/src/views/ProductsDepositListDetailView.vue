<template>
  <div class="container" v-if="deposit">
    <h2 class="mb-4">{{ deposit.fin_prdt_nm }} 상세 정보</h2>
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">{{ deposit.kor_co_nm }}</h5>
        <div>
          <span class="ml-2">좋아요 {{ likeCount }}개 </span>
          <button @click="toggleLike" :class="{ 'btn-primary': isLiked, 'btn-secondary': !isLiked }">❤️
            {{ isLiked ? '좋아요 취소' : '좋아요' }}
          </button>
        </div>
        <!-- 기존 상품 정보 표시 부분 -->
        <p class="card-text">
          <strong>가입 방법:</strong> {{ deposit.join_way }}<br>
          <strong>가입 대상:</strong> {{ deposit.join_member }}<br>
          <strong>가입 금액:</strong> {{ formatJoinPrice(deposit.join_price) }}<br>
          <strong>이자율 종류:</strong> {{ deposit.intr_rate_type_nm }}<br>
          <strong>적립 유형:</strong> {{ deposit.rsrv_type_nm }}<br>
          <strong>저축 기간:</strong> {{ deposit.save_trm }}개월<br>
          <strong>기본 이자율:</strong> {{ deposit.intr_rate }}%<br>
          <strong>우대 이자율:</strong> {{ deposit.intr_rate2 }}%<br>
          <strong>나이 제한:</strong> {{ formatAgeRange(deposit.age_range) }}
        </p>
        <div v-if="deposit.etc_note">
          <strong>기타 유의사항:</strong>
          <p>{{ deposit.etc_note }}</p>
        </div>
        
        <!-- 댓글 섹션 추가 -->
        <div class="mt-4">
          <h4>댓글</h4>
          <ul class="list-unstyled">
            <li v-for="comment in comments" :key="comment.id" class="mb-2">
              <strong>{{ comment.user }}:</strong> {{ comment.content }}
            </li>
          </ul>
          <form @submit.prevent="addComment" class="mt-3">
            <div class="form-group">
              <textarea v-model="newComment" class="form-control" rows="3" placeholder="댓글을 입력하세요"></textarea>
            </div>
            <button type="submit" class="btn btn-primary">댓글 작성</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRoute } from 'vue-router';
import { useCounterStore } from '@/stores/counter';

const route = useRoute();
const store = useCounterStore();
const deposit = ref(null);
const isLiked = ref(false);
const likeCount = ref(0);
const comments = ref([]);
const newComment = ref('');

// axios 요청에 인증 토큰 추가
const getConfig = () => ({
  headers: {
    'Authorization': `Token ${store.token}`,
    'X-CSRFToken': document.cookie.match(/csrftoken=([\w-]+)/)?.[1]
  },
  withCredentials: true
});

const fetchDepositDetail = async () => {
  try {
    const response = await axios.get(
      `${store.API_URL}/api/products/deposit-products/${route.params.id}/`,
      {
        headers: {
          'Authorization': `Token ${store.token}`
        }
      }
    );
    deposit.value = response.data;
    isLiked.value = response.data.is_liked;  // 좋아요 상태 설정
    likeCount.value = response.data.like_count;  // 좋아요 개수 설정
  } catch (error) {
    console.error('예금 상품 상세 정보를 불러오는 중 오류가 발생했습니다:', error);
  }
};

const toggleLike = async () => {
  if (!store.isLogin) {
    alert('로그인이 필요한 서비스입니다.');
    router.push('/login');
    return;
  }
  
  try {
    const response = await axios.post(
      `${store.API_URL}/api/products/deposit-products/${route.params.id}/like/`,
      {},
      {
        headers: {
          'Authorization': `Token ${store.token}`
        }
      }
    );
    isLiked.value = response.data.is_liked;
    likeCount.value = response.data.like_count;
  } catch (error) {
    console.error('좋아요 처리 중 오류가 발생했습니다:', error);
  }
};

const addComment = async () => {
  if (newComment.value.trim() === '') return;
  try {
    const response = await axios.post(
      `${store.API_URL}/api/products/deposit-products/${route.params.id}/comment/add/`,
      { content: newComment.value },
      {
        headers: {
          'Authorization': `Token ${store.token}`
        }
      }
    );
    comments.value.push(response.data);
    newComment.value = '';
  } catch (error) {
    console.error('댓글 작성 중 오류가 발생했습니다:', error);
  }
};

const fetchComments = async () => {
  if (!store.isLogin) {
    return;  // 로그인하지 않은 경우 API 호출하지 않음
  }
  try {
    const response = await axios.get(
      `${store.API_URL}/api/products/deposit-products/${route.params.id}/comments/`,
      {
        headers: {
          'Authorization': `Token ${store.token}`
        }
      }
    );
    comments.value = response.data;
  } catch (error) {
    console.error('댓글을 불러오는 중 오류가 발생했습니다:', error);
  }
};

const formatJoinPrice = (price) => {
  try {
    if (Array.isArray(price)) {
      return `${price[0]}만원 ~ ${price[1]}만원`;
    } else if (typeof price === 'string') {
      const [min, max] = price.split(',').map(num => num.trim());
      return `${min}만원 ~ ${max}만원`;
    } else if (typeof price === 'number') {
      return `${price}만원`;
    } else if (price === null || price === undefined) {
      return '가입 금액 정보 없음';
    }
    // 예외적인 경우 처리
    return '알 수 없는 형식';
  } catch (error) {
    console.error('가입 금액 형식 변환 중 오류:', error);
    return '가입 금액 정보 없음';
  }
};

const formatAgeRange = (range) => {
  if (!range) return '제한 없음';
  const [min, max] = range.split(', ');
  return `${min}세 ~ ${max}세`;
};

onMounted(() => {
  fetchDepositDetail();  // 기본 상품 정보는 항상 가져옴
  if (store.isLogin) {   // 로그인한 경우에만 댓글과 좋아요 정보를 가져옴
    fetchComments();
  }
});
</script>

<style scoped>
.card {
  margin-top: 20px;
}
</style>

<!-- <template>
  <div class="container">
    <h1>예금 상품 상세 조회</h1>
    <div v-if="product" class="card">
      <div class="card-body">
        <h2 class="card-title">{{ product.fin_prdt_nm }}</h2>
        <div class="card-text">
          <p><strong>금융회사:</strong> {{ product.kor_co_nm }}</p>
          <p><strong>가입방법:</strong> {{ product.join_way }}</p>
          <p><strong>가입대상:</strong> {{ product.join_member }}</p>
          <p><strong>가입금액:</strong> {{ product.join_price }}원</p>
          <p><strong>금리유형:</strong> {{ product.intr_rate_type_nm }}</p>
          
          <h3>금리 정보</h3>
          <table class="table">
            <thead>
              <tr>
                <th>저축 기간</th>
                <th>기본 금리</th>
                <th>우대 금리</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="detail in product.save_trm_rates" :key="detail.save_trm">
                <td>{{ detail.save_trm }}개월</td>
                <td>{{ detail.intr_rate }}%</td>
                <td>{{ detail.intr_rate2 }}%</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    <div v-else class="alert alert-info">
      상품 정보를 불러오는 중입니다...
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const router = useRouter();
const product = ref(null);

const fetchProductDetails = async () => {
  try {
    // URL에서 fin_prdt_nm을 사용
    const response = await axios.get(`http://localhost:8000/api/deposit-products/${encodeURIComponent(route.params.fin_prdt_nm)}/`);
    product.value = response.data;
  } catch (error) {
    console.error('상품 정보를 불러오는 중 오류가 발생했습니다:', error);
    router.push('/productsdepositlist');
  }
};

onMounted(() => {
  fetchProductDetails();
});
</script> -->