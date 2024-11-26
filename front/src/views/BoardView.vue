<template>
  <div class="main-container">
    <h1 class="board-title">똑!똑! 게시판</h1>
      <div class="article-container">
        <div class="header-container">
          <h2 class="h2">게시글 목록</h2>
          <RouterLink 
            v-if="isAdmin" 
            :to="{ name: 'create' }"
            class="create-btn"
          >
            CREATE
          </RouterLink>
        </div>
        <BoardArticleListView 
          :articles="store.articles" 
          :isLoading="store.isLoading" 
          :formatDate="formatDate" 
        />
    </div>
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
.article-container{
  margin: 2% 12% 16% 12%;
  padding: 0% 0% 8% 0%;
}
.board-title {
  text-align: center;
  margin: 2rem 0;  /* 상하 여백 증가 */
  padding: 10px;
  font-size: 3rem;
  font-weight: bold;
}

.h1 {
  margin: 0;
  padding: 10px 60px;
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 10px;
}

.h2 {
  margin: 0;
}

.create-btn {
  display: inline-block;
  padding: 8px 16px;
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