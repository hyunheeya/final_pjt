<template>
  <div>
    <h1>예적금 전체 상품 리스트</h1>
    <div>
      <a @click="showComponent('deposit')">예금</a> | 
      <a @click="showComponent('savings')">적금</a>
    </div>
    <ProductsDepositListView v-if="currentView === 'deposit'" />
    <ProductsSavingsListView v-if="currentView === 'savings'" />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import ProductsDepositListView from '@/components/ProductsDepositListView.vue';
import ProductsSavingsListView from '@/components/ProductsSavingsListView.vue';

const currentView = ref(null);

const showComponent = (view) => {
  currentView.value = view;
};
</script>

<style scoped>
button {
  margin-right: 10px;
  padding: 5px 10px;
  cursor: pointer;
}
</style>