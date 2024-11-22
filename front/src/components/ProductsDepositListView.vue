<template>
  <div class="container">
    <h2 class="mb-4">예금 전체 상품 조회</h2>
    <div v-for="(products, productName) in groupedProducts" :key="productName" class="mb-4">
      <h3>{{ productName }}</h3>
      <div class="row row-cols-1 row-cols-md-3 g-4">
        <div v-for="product in products" :key="product.id" class="col">
          <div class="card h-100">
            <div class="card-body">
              <h5 class="card-title">{{ product.kor_co_nm }}</h5>
              <p class="card-text">
                <strong>저축 기간:</strong> {{ product.save_trm }}개월<br>
                <strong>기본 금리:</strong> {{ product.intr_rate }}%<br>
              </p>
              <RouterLink 
                :to="{ name: 'productsdepositlistdetail', params: { id: product.id } }" 
                class="btn btn-primary"
              >
                상세 정보
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
      <hr>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';

const depositProducts = ref([]);

const groupedProducts = computed(() => {
  const grouped = {};
  depositProducts.value.forEach(product => {
    if (!grouped[product.fin_prdt_nm]) {
      grouped[product.fin_prdt_nm] = [];
    }
    grouped[product.fin_prdt_nm].push(product);
  });
  return grouped;
});

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