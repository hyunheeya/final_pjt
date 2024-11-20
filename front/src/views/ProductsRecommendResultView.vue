<template>
  <div>
    <h1>추천 결과</h1>
    <ul>
      <li v-for="result in results" :key="result.name">
        {{ result.name }} - 금리: {{ result.interest_rate }}%
      </li>
    </ul>
    <router-link :to="{ name: 'productsrecommend' }">
      <button>다시 추천받기</button>
    </router-link>
  </div>
</template>

<script>
export default {
  props: {
    results: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped>
/* 스타일 추가 */
</style>
