<template>
  <div>
    <h1>추천 결과</h1>
    <ul>
      <li v-for="result in results" :key="result.name">
        <p><strong>금융회사:</strong> {{ result.name }}</p>
        <p><strong>금리:</strong> {{ result.interest_rate }}%</p>
        <p><strong>납입 기간:</strong> {{ result.save_trm }}</p>
        <!-- <div>
          <router-link :to="{ name: 'productsdepositlistdetail' }">
            <button>Detail</button>
          </router-link>
        </div> -->
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
