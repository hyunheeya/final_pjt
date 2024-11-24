<template>
  <div>
    <h1>톡!톡! 게시판</h1>
    <RouterLink v-if="isAdmin" :to="{ name: 'create' }">
      [CREATE]
    </RouterLink>
    <h2>게시글 목록</h2>
    <BoardArticleListView 
      :articles="store.articles" 
      :isLoading="store.isLoading" 
      :formatDate="formatDate" 
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'
import BoardArticleListView from '@/views/BoardArticleListView.vue'  // import 추가

const store = useCounterStore()
const isAdmin = ref(false)

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return `${date.getFullYear()}년 ${date.getMonth() + 1}월 ${date.getDate()}일`
}

onMounted(async () => {
  await store.fetchArticles()
  isAdmin.value = await store.checkAdminStatus()
})
</script>

<style scoped>

</style>
