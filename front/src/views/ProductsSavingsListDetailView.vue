<template>
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
</style>