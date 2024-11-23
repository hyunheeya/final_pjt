<template>
  <div>
    <h1>예적금 전체 상품 리스트</h1>
    <div>
      <button @click="showComponent('deposit')" :class="{ active: currentView === 'deposit' }">예금</button>
      <button @click="showComponent('savings')" :class="{ active: currentView === 'savings' }">적금</button>
    </div>
    <ProductsDepositListView v-if="currentView === 'deposit'" />
    <ProductsSavingsListView v-if="currentView === 'savings'" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import ProductsDepositListView from '@/components/ProductsDepositListView.vue';
import ProductsSavingsListView from '@/components/ProductsSavingsListView.vue';

const route = useRoute();
const router = useRouter();

// 쿼리 파라미터를 확인해 초기 상태 설정
const currentView = ref(route.query.tab || 'deposit');

const showComponent = (view) => {
  currentView.value = view;
  router.push({ query: { tab: view } }); // 쿼리 파라미터 업데이트
};

onMounted(() => {
  if (!route.query.tab) {
    showComponent('deposit'); // 기본값은 예금
  }
});
</script>

<style scoped>
button {
  margin-right: 10px;
  padding: 5px 10px;
  cursor: pointer;
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button.active {
  background-color: #007bff;
  color: white;
}
</style>

<!-- <template>
  <div>
    <h1>예적금 전체 상품 리스트</h1>
    <div>
      <button @click="showComponent('deposit')" :class="{ active: currentView === 'deposit' }">예금</button>
      <button @click="showComponent('savings')" :class="{ active: currentView === 'savings' }">적금</button>
    </div>
    <ProductsDepositListView v-if="currentView === 'deposit'" />
    <ProductsSavingsListView v-if="currentView === 'savings'" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ProductsDepositListView from '@/components/ProductsDepositListView.vue'
import ProductsSavingsListView from '@/components/ProductsSavingsListView.vue'

const currentView = ref('deposit')

const showComponent = (view) => {
  currentView.value = view;
};

// 첫 화면은 예금을 보여주기
onMounted(() => {
  showComponent('deposit');
});
</script>

<style scoped>
button {
  margin-right: 10px;
  padding: 5px 10px;
  cursor: pointer;
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button.active {
  background-color: #007bff;
  color: white;
}
</style> -->