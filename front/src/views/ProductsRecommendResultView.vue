<template>
  <div class="container">
    <h1 class="text-center mb-4">추천 결과</h1>
    <div class="row justify-content-end">
      <div v-for="result in results" :key="result.name" class="col-md-4 mb-4">
        <div class="card">
          <div class="card-body text-end">
            <h5 class="card-title fw-bold mb-3">{{ result.name }}</h5>
            <p class="mb-2">
              <span class="label">금리: </span>
              <span class="value">{{ result.interest_rate }}%</span>
            </p>
            <p class="mb-2">
              <span class="label">납입 기간: </span>
              <span class="value">{{ result.save_trm }}개월</span>
            </p>
            <p class="mb-2">
              <span class="label">추천 점수: </span>
              <span class="value">{{ result.weight }}</span>
            </p>
            <RouterLink 
              :to="{ 
                name: result.product_type === '예금' ? 'productsdepositlistdetail' : 'productssavingslistdetail',
                params: { id: result.id }
              }" 
              class="btn btn-primary"
            >
              Detail
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
    <div class="text-end mt-4">
      <RouterLink :to="{ name: 'productsrecommend' }" class="btn btn-primary">
        다시 추천받기
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  results: {
    type: Array,
    required: true
  }
})
</script>

<style scoped>
/* 스타일 추가 */
.text-end {
  text-align: right;
}

.card {
  transition: transform 0.3s;
}

.card:hover {
  transform: translateY(-5px);
}

.btn {
  margin-top: 1rem;
}
</style>
