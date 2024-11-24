<template>
  <div>
    <h1>톡!톡! 게시판</h1>
    <!-- 관리자인 경우에만 CREATE 버튼 표시 -->
    <RouterLink 
      v-if="isAdmin"
      :to="{ name: 'create' }"
    >
      [CREATE]
    </RouterLink>
    <h2>게시글 목록</h2>
    <BoardArticleListView :articles="articles" :formatDate="formatDate" />
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import BoardArticleListView from '@/views/BoardArticleListView.vue'
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const articles = ref([])
const isAdmin = ref(false)

// 관리자 여부 확인
const checkAdminStatus = async () => {
  try {
    const response = await axios({
      method: 'get',
      url: `${store.API_URL}/api/board/check-admin/`,
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
    isAdmin.value = response.data.is_admin
  } catch (err) {
    console.log(err)
  }
}

onMounted(() => {
  checkAdminStatus()
})

const getArticles = function() {
  axios({
    method: 'get',
    url: `${store.API_URL}/api/board/articles/`,
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
  .then((res) => {
    articles.value = res.data
  })
  .catch((err) => {
    console.log(err)
  })
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return `${date.getFullYear()}년 ${date.getMonth() + 1}월 ${date.getDate()}일`
}

onMounted(() => {
  getArticles()
})
</script>

<style scoped>

</style>
