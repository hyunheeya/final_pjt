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
import ProductsDepositListView from '@/components/ProductsDepositListView.vue';
import ProductsSavingsListView from '@/components/ProductsSavingsListView.vue';

const currentView = ref('deposit');

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
</style>