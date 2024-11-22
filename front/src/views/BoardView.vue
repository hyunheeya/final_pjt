<template>
  <div>
    <h1>톡!톡! 게시판</h1>
    <RouterLink :to="{ name: 'create' }">
      [CREATE]
    </RouterLink>
    <hr>
    <BoardArticleView />
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import BoardArticleView from '@/components/BoardArticleView.vue'
</script>

<style scoped>

</style>