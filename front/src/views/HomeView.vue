<template>
  <div>
    <h1>메인 페이지</h1>
    <div v-if="store.isLogin">
      <p v-if="username">{{ username }}님 환영합니다!</p>
      <p v-else>로그인을 해주세요.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useCounterStore } from "@/stores/counter";

const store = useCounterStore();
const username = computed(() => store.userInfo?.username);

onMounted(async () => {
  if (store.isLogin) {
    await store.getUserInfo();
  }
});
</script>

<style scoped>
</style>