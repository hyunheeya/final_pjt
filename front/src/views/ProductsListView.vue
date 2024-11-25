<template>
  <div>
    <h1 class="h1">예적금 전체 상품 리스트</h1>
    <!-- 예금/적금 탭 -->
    <div class="product-tabs">
      <button 
        @click="showComponent('deposit')" 
        :class="['tab-button', currentView === 'deposit' ? 'active' : '']"
      >
        예금
      </button>
      <button 
        @click="showComponent('savings')" 
        :class="['tab-button', currentView === 'savings' ? 'active' : '']"
      >
        적금
      </button>
    </div>

    <!-- 컴포넌트 표시 영역 -->
    <div class="tab-content">
      <ProductsDepositListView v-if="currentView === 'deposit'" />
      <ProductsSavingsListView v-if="currentView === 'savings'" />
    </div>
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
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.title {
  font-size: 1.75rem;
  margin-bottom: 2rem;
}

.product-tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid #e9ecef;
}

.tab-button {
  padding: 0.75rem 2rem;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 1rem;
}

.tab-button.active {
  color: #ffc107;
  border-bottom: 2px solid #ffc107;
}

.h1{
  margin: 0px;
  padding: 25px;
}

</style>