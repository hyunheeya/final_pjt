<template>
  <header>
    <nav>
    <RouterLink :to="{name:'home'}">Home</RouterLink> | 
    <RouterLink :to="{name:'productsrecommend'}">예적금 상품 추천</RouterLink> | 
    <RouterLink :to="{name:'productslist'}">예적금 상품 전체 리스트</RouterLink> | 
    <RouterLink :to="{name:'signup'}">회원가입</RouterLink> | 
    <RouterLink :to="{name:'login'}">로그인</RouterLink> | 
    <!-- parmas -->
    <RouterLink :to="{name:'profile'}">마이페이지</RouterLink> 
    </nav>
  </header>

  <RouterView />
</template>

<script setup>

</script>

<style scoped>

</style>