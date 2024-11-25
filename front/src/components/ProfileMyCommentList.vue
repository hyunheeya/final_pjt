<template>
  <div class="container">
    <h2 class="mb-4">내가 작성한 댓글</h2>
    <div class="mb-4">
      <button 
        @click="currentView = 'deposit'" 
        :class="['btn', 'me-2', currentView === 'deposit' ? 'btn-warning' : 'btn-outline-secondary']"
      >
        예금
      </button>
      <button 
        @click="currentView = 'savings'"
        :class="['btn', 'me-2', currentView === 'savings' ? 'btn-warning' : 'btn-outline-secondary']"
      >
        적금
      </button>
    </div>

    <!-- 예금 댓글 목록 -->
    <div v-if="currentView === 'deposit'" class="comment-list">
      <div v-for="comment in depositComments" :key="comment.id" class="card mb-3">
        <div class="card-body">
          <h5 class="card-title">{{ comment.deposit__fin_prdt_nm }}</h5>
          <h6 class="card-subtitle mb-2 text-muted">{{ comment.deposit__kor_co_nm }}</h6>
          <p class="card-text">{{ comment.content }}</p>
          <div class="d-flex justify-content-between align-items-center">
            <small class="text-muted">{{ formatDate(comment.created_at) }}</small>
            <RouterLink 
              :to="{ name: 'productsdepositlistdetail', params: { id: comment.deposit__id }}"
              class="btn btn-sm btn-warning"
            >
              상품 보기
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
    <p v-else class="text-center text-muted">내가 쓴 댓글이 없습니다.</p>


    <!-- 적금 댓글 목록 -->
    <div v-if="currentView === 'savings'" class="comment-list">
      <div v-for="comment in savingsComments" :key="comment.id" class="card mb-3">
        <div class="card-body">
          <h5 class="card-title">{{ comment.savings__fin_prdt_nm }}</h5>
          <h6 class="card-subtitle mb-2 text-muted">{{ comment.savings__kor_co_nm }}</h6>
          <p class="card-text">{{ comment.content }}</p>
          <div class="d-flex justify-content-between align-items-center">
            <small class="text-muted">{{ formatDate(comment.created_at) }}</small>
            <RouterLink 
              :to="{ name: 'productssavingslistdetail', params: { id: comment.savings__id }}"
              class="btn btn-sm btn-warning"
            >
              상품 보기
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
    <p v-else class="text-center text-muted">내가 쓴 댓글이 없습니다.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import useCounterStore from '@/stores/counter';

const store = useCounterStore();
const currentView = ref('deposit');
const depositComments = ref([]);
const savingsComments = ref([]);

const fetchComments = async () => {
  try {
    const response = await axios.get(`${store.API_URL}/api/accounts/user-comments/`, {
      headers: { Authorization: `Token ${store.token}` }
    });
    depositComments.value = response.data.deposit_comments;
    savingsComments.value = response.data.savings_comments;
  } catch (error) {
    console.error('댓글 조회 실패:', error);
  }
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString();
};

onMounted(() => {
  fetchComments();
});
</script>