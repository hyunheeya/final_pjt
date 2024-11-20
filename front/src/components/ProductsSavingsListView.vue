<!-- <template>
  <div>
    <h2>적금 전체 상품 조회</h2>
    <RouterLink :to="{name:'productssavingslistdetail'}">적금 상품 상세 조회 하기</RouterLink>
  </div>
</template>

<script setup>

</script>

<style scoped>

</style> -->

<template>
  <div class="container">
    <h2 class="mb-4">적금 전체 상품 조회</h2>
    <div class="row row-cols-1 row-cols-md-3 g-4">
      <div v-for="product in savingsProducts" :key="product.id" class="col">
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">{{ product.fin_prdt_nm }}</h5>
            <p class="card-text">
              <strong>금융회사:</strong> {{ product.kor_co_nm }}<br>
              <strong>기본 금리:</strong> {{ product.intr_rate }}%<br>
              <strong>저축 기간:</strong> {{ product.save_trm }}개월<br>
              <strong>적립 유형:</strong> {{ product.rsrv_type_nm }}
            </p>
            <RouterLink 
              :to="{ name: 'productssavingslistdetail', params: { id: product.id } }" 
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

const savingsProducts = ref([]);

const fetchSavingsProducts = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/savings-products/');
    savingsProducts.value = response.data;
  } catch (error) {
    console.error('적금 상품을 불러오는 중 오류가 발생했습니다:', error);
  }
};

onMounted(() => {
  fetchSavingsProducts();
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