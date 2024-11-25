<template>
  <div>
    <h1 class="h1">톡!톡! 게시판</h1>
    <RouterLink 
      v-if="isAdmin" 
      :to="{ name: 'create' }"
      class="create-btn"
    >
      CREATE
    </RouterLink>
    <h2 class="h2">게시글 목록</h2>
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
import BoardArticleListView from '@/components/BoardArticleListView.vue'  // import 추가

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
  .h1, .h2{
    margin: 0%;
    padding: 10px 60px;
  }

  .create-btn {
  display: inline-block;
  padding: 8px 16px;
  margin: 0 60px;
  background-color: #4CAF50;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-weight: 600;
  transition: background-color 0.3s ease;
}

.create-btn:hover {
  background-color: #45a049;
}

</style>
