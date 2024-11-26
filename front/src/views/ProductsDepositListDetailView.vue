<template>
  <div class="container" v-if="deposit">
    <h2 class="mb-4">{{ deposit.fin_prdt_nm }} 상세 정보</h2>
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">
          <img :src="`/bank_logo/${deposit.kor_co_nm}.png`" alt="은행 로고" />
          {{ deposit.kor_co_nm }}
        </h5>
        <div>
          <button 
            @click="toggleLike" 
            :class="isLiked ? 'btn-danger' : 'btn-outline-danger'" 
            class="btn"
          >
            ❤️ {{ likeCount }}
          </button>
        </div>
        <!-- 기존 상품 정보 표시 부분 -->
        <p class="card-text">
          <strong>가입 방법:</strong> {{ deposit.join_way }}<br>
          <strong>가입 대상:</strong> {{ deposit.join_member }}<br>
          <strong>가입 금액:</strong> {{ formatJoinPrice(deposit.join_price) }}<br>
          <strong>이자율 종류:</strong> {{ deposit.intr_rate_type_nm }}<br>
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
              <div>
                <strong>{{ comment.user }}:</strong> {{ comment.content }} 
              </div>
              <span>{{ comment.created_at }}</span>
              <button 
                v-if="store.isLogin && store.userInfo && comment.user === store.userInfo.username" 
                @click="deleteComment(comment.id)" 
                class="btn btn-danger btn-sm ms-2"
              >
                삭제
              </button>
            </li>
          </ul>
          <form @submit.prevent="addComment" class="mt-3">
            <div class="form-group">
              <textarea v-model="newComment" class="form-control" rows="3" placeholder="댓글을 입력하세요"></textarea>
            </div>
            <button type="submit" class="btn btn-warning">댓글 작성</button>
          </form>
        </div>
      </div>
    </div>
    <div class="mt-3">
      <button @click="goBack" class="btn btn-secondary">목록으로 돌아가기</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import { useCounterStore } from '@/stores/counter';

const route = useRoute();
const router = useRouter();
const store = useCounterStore();
const deposit = ref(null);
const isLiked = ref(false);
const likeCount = ref(0);
const comments = ref([]);
const newComment = ref('');

// 예금 상세 정보 가져오기
const fetchDepositDetail = async () => {
  try {
    const response = await axios.get(
      `${store.API_URL}/api/products/deposit-products/${route.params.id}/`,
      {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      }
    );
    deposit.value = response.data;
    isLiked.value = response.data.is_liked; // 좋아요 상태 설정
    likeCount.value = response.data.like_count; // 좋아요 개수 설정
  } catch (error) {
    console.error('예금 상품 상세 정보를 불러오는 중 오류가 발생했습니다:', error);
  }
};

// 좋아요 상태 토글
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
          Authorization: `Token ${store.token}`,
        },
      }
    );
    isLiked.value = response.data.is_liked; // 좋아요 상태 업데이트
    likeCount.value = response.data.like_count; // 좋아요 개수 업데이트
  } catch (error) {
    console.error('좋아요 처리 중 오류가 발생했습니다:', error);
  }
};

// 댓글 추가
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

// 댓글 조회
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

// 댓글 삭제
const deleteComment = async (commentId) => {
  if (!confirm('댓글을 삭제하시겠습니까?')) return;
  
  try {
    await axios.delete(
      `${store.API_URL}/api/products/deposit-products/${route.params.id}/comment/${commentId}/delete/`,
      {
        headers: {
          'Authorization': `Token ${store.token}`
        }
      }
    );
    // 댓글 목록에서 삭제된 댓글 제거
    comments.value = comments.value.filter(comment => comment.id !== commentId);
  } catch (error) {
    console.error('댓글 삭제 중 오류가 발생했습니다:', error);
    alert('댓글 삭제에 실패했습니다.');
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

// 이전 페이지로 돌아가기
const goBack = () => {
  router.push({ name: 'productslist' }); // 라우터 이름으로 이동
};

onMounted(async () => {
  try {
    await store.getUserInfo(); // 사용자 정보 로드
    fetchDepositDetail(); // 예금 상세 정보 가져오기
    if (store.isLogin) {
      fetchComments(); // 댓글 목록 가져오기
    }
  } catch (error) {
    console.error('초기 데이터 로드 중 오류가 발생했습니다:', error);
  }
});

</script>

<style scoped>
.card {
  margin-top: 20px;
}

.card-title img {
  height: 40px;
  width: auto;
  margin-right: 10px;
}
.card-text{
  margin-bottom: 60px;
}
</style>