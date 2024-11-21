<template>
  <header>
    <nav>
      <RouterLink :to="{name:'home'}">Home</RouterLink> | 
      <RouterLink :to="{name:'productsrecommend'}">예적금 상품 추천</RouterLink> | 
      <RouterLink :to="{name:'productslist'}">예적금 상품 전체 리스트</RouterLink> |

      <!-- 로그인 안 한 경우 -->
      <div v-if="!isLogin">
        <RouterLink :to="{name:'signup'}">회원가입</RouterLink> | 
        <RouterLink :to="{name:'login'}">로그인</RouterLink>
      </div>

      <!-- 로그인 한 경우 -->
      <div v-if="isLogin">
        <RouterLink :to="{name:'profile'}">마이페이지</RouterLink> |
        <button @click="logOut">로그아웃</button>
      </div>
    </nav>
  </header>

  <RouterView />
</template>

<script setup>
  import { useCounterStore } from "@/stores/counter";
  import { computed } from 'vue';

  const store = useCounterStore();
  const isLogin = computed(() => store.isLogin);
  const logOut = store.logOut;
</script>


<style scoped>

</style>