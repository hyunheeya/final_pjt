<template>
  <div class="container" v-if="savings">
    <h2 class="mb-4">{{ savings.fin_prdt_nm }} 상세 정보</h2>
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">{{ savings.kor_co_nm }}</h5>
        <button 
            @click="toggleLike" 
            :class="isLiked ? 'btn-danger' : 'btn-outline-danger'" 
            class="btn"
          >
            ❤️ {{ likeCount }}
          </button>
        <p class="card-text">
          <strong>가입 방법:</strong> {{ savings.join_way }}<br>
          <strong>가입 대상:</strong> {{ savings.join_member }}<br>
          <strong>적립 유형:</strong> {{ savings.rsrv_type_nm }}<br>
          <strong>저축 기간:</strong> {{ savings.save_trm }}개월<br>
          <strong>기본 금리:</strong> {{ savings.intr_rate }}%<br>
          <strong>우대 금리:</strong> {{ savings.intr_rate2 }}%<br>
          <strong>가입 나이:</strong> {{ formatAgeRange(savings.age_range) }}<br>
          <strong>가입 금액:</strong> {{ formatJoinPrice(savings.join_price) }}<br>
          <strong>기타 유의사항:</strong> {{ savings.etc_note }}
        </p>

        <!-- 댓글 섹션 추가 -->
        <div class="mt-4">
          <h4>댓글</h4>
          <ul class="list-unstyled">
            <li v-for="comment in comments" :key="comment.id" class="mb-2">
              <strong>{{ comment.user }}:</strong> {{ comment.content }}
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

const savings = ref(null); // 적금 상품 정보
const isLiked = ref(false); // 좋아요 상태
const likeCount = ref(0); // 좋아요 개수
const comments = ref([]); // 댓글 목록
const newComment = ref(''); // 새로운 댓글 내용

// 적금 상세 정보 가져오기
const fetchSavingsDetail = async () => {
  try {
    const response = await axios.get(
      `${store.API_URL}/api/products/savings-products/${route.params.id}/`,
      {
        headers: { Authorization: `Token ${store.token}` },
      }
    );
    savings.value = response.data;
    isLiked.value = response.data.is_liked;
    likeCount.value = response.data.like_count;
  } catch (error) {
    console.error('적금 상품 상세 정보를 불러오는 중 오류가 발생했습니다:', error);
  }
};

// 좋아요 상태 토글
const toggleLike = async () => {
  if (!store.isLogin) {
    alert('로그인이 필요한 서비스입니다.');
    return;
  }

  try {
    const response = await axios.post(
      `${store.API_URL}/api/products/savings-products/${route.params.id}/like/`,
      {},
      {
        headers: { Authorization: `Token ${store.token}` },
      }
    );
    isLiked.value = response.data.is_liked;
    likeCount.value = response.data.like_count;

    // 좋아요 이후 사용자 정보 갱신
    await store.getUserInfo();
  } catch (error) {
    console.error('좋아요 처리 중 오류가 발생했습니다:', error);
  }
};

// 좋아요 상태 가져오기
const fetchLikeStatus = async () => {
  try {
    const response = await axios.get(
      `${store.API_URL}/api/products/savings-products/${route.params.id}/like-status/`,
      {
        headers: { Authorization: `Token ${store.token}` },
      }
    );
    isLiked.value = response.data.is_liked;
    likeCount.value = response.data.like_count;
  } catch (error) {
    console.error('좋아요 상태를 불러오는 중 오류 발생:', error);
  }
};

// 댓글 작성
const addComment = async () => {
  if (newComment.value.trim() === '') return;
  try {
    const response = await axios.post(
      `${store.API_URL}/api/products/savings-products/${route.params.id}/comment/add/`,
      { content: newComment.value },
      {
        headers: { Authorization: `Token ${store.token}` },
      }
    );
    comments.value.push(response.data);
    newComment.value = '';
  } catch (error) {
    console.error('댓글 작성 중 오류가 발생했습니다:', error);
  }
};

// 댓글 삭제
const deleteComment = async (commentId) => {
  if (!confirm('댓글을 삭제하시겠습니까?')) return;
  
  try {
    await axios.delete(
      `${store.API_URL}/api/products/savings-products/${route.params.id}/comment/${commentId}/delete/`,
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

// 댓글 목록 가져오기
const fetchComments = async () => {
  if (!store.isLogin) return;
  try {
    const response = await axios.get(
      `${store.API_URL}/api/products/savings-products/${route.params.id}/comments/`,
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

// 가격 데이터 변환
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


// 나이 데이터 변환
const formatAgeRange = (ageRange) => {
  try {
    if (Array.isArray(ageRange)) {
      return `${ageRange[0]}세 ~ ${ageRange[1]}세`;
    }
    else if (typeof ageRange === 'string') {
      const [min, max] = ageRange.split(',').map(num => num.trim());
      return `${min}세 ~ ${max}세`;
    }
    return ageRange;
  } catch (error) {
    console.error('나이 범위 형식 변환 중 오류:', error);
    return '나이 제한 정보 없음';
  }
};

// 이전 페이지로 돌아가기
//쿼리 파라미터를 읽어 currentView를 savings로 설정
const goBack = () => {
  router.push({ name: 'productslist', query: { tab: 'savings' } });
};


// 컴포넌트 로드 시 데이터 가져오기
onMounted(async () => {
  await store.getUserInfo(); // 사용자 정보 로드
  fetchSavingsDetail();
  fetchLikeStatus();
  if (store.isLogin) {
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
  <div class="container" v-if="savings">
    <h2 class="mb-4">{{ savings.fin_prdt_nm }} 상세 정보</h2>
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">{{ savings.kor_co_nm }}</h5>
        <p class="card-text">
          <strong>가입 방법:</strong> {{ savings.join_way }}<br>
          <strong>가입 대상:</strong> {{ savings.join_member }}<br>
          <strong>적립 유형:</strong> {{ savings.rsrv_type_nm }}<br>
          <strong>저축 기간:</strong> {{ savings.save_trm }}개월<br>
          <strong>기본 금리:</strong> {{ savings.intr_rate }}%<br>
          <strong>우대 금리:</strong> {{ savings.intr_rate2 }}%<br>
          <strong>가입 나이:</strong> {{ savings.age_range }}세<br>
          <strong>가입 금액:</strong> {{ savings.join_price }}만원<br>
          <strong>기타 유의사항:</strong> {{ savings.etc_note }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRoute } from 'vue-router';

const route = useRoute();
const savings = ref(null);

const fetchSavingsDetail = async () => {
  try {
    const response = await axios.get(`http://localhost:8000/api/savings-products/${route.params.id}/`);
    savings.value = response.data;
  } catch (error) {
    console.error('적금 상품 상세 정보를 불러오는 중 오류가 발생했습니다:', error);
  }
};

onMounted(() => {
  fetchSavingsDetail();
});
</script>

<style scoped>
.card {
  margin-top: 20px;
}
</style> -->