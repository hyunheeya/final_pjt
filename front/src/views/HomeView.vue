<template>
  <div>
    <h1>메인 페이지</h1>
  </div>
</template>

<script setup>
import { onMounted} from 'vue';
import { useCounterStore } from "@/stores/counter";

const store = useCounterStore();

// onMounted에서 로그인 여부 확인 후 사용자 정보 요청
onMounted(async () => {
  if (store.isLogin) {
    try {
      await store.getUserInfo();
    } catch (error) {
      console.error("사용자 정보를 불러오는 데 실패했습니다:", error);
    }
  }
});
</script>

<style scoped>
</style>
