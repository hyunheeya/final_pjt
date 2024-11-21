<template>
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
</script>