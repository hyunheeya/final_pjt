<template>
  <div class="container">
    <h2 class="mb-4">예금 전체 상품 조회</h2>
    <div class="row row-cols-1 row-cols-md-3 g-4">
      <div v-for="product in depositProducts" :key="product.fin_prdt_nm" class="col">
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
            name: 'productsdepositlistdetail', 
            params: { fin_prdt_nm: product.fin_prdt_nm } 
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

  const depositProducts = ref([]);

  const fetchDepositProducts = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/deposit-products/');
      depositProducts.value = response.data;
    } catch (error) {
      console.error('예금 상품을 불러오는 중 오류가 발생했습니다:', error);
    }
  };

  onMounted(() => {
    fetchDepositProducts();
  });
</script>