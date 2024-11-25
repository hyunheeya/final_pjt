<template>
  <div>
    <div v-if="article">
      <h3>{{ article.title }}</h3>
      <p>{{ article.content }}</p>
      <div v-if="article.image" class="image-container">
        <img :src="getImageUrl(article.image)" :alt="article.title">
      </div>
      <span>{{ formatDate(article.created_at) }}</span>
      <div>
        <button @click="articleList" class="btn btn-primary">
          목록
        </button>
      </div>
      <!-- 관리자인 경우에만 수정/삭제 버튼 표시 -->
      <div v-if="isAdmin" class="button-group">
        <RouterLink 
          :to="{ name: 'edit', params: { id: article.id }}" 
          class="edit-btn"
        >
          수정
        </RouterLink>
        <button @click="deleteArticle" class="delete-btn">
          삭제
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const route = useRoute()
const router = useRouter()
const article = ref(null)
const isAdmin = ref(false)

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

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return `${date.getFullYear()}년 ${date.getMonth() + 1}월 ${date.getDate()}일`
}

const getArticle = function() {
  axios({
    method: 'get',
    url: `${store.API_URL}/api/board/articles/${route.params.id}/`,
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
  .then((res) => {
    article.value = res.data
  })
  .catch((err) => {
    console.log(err)
  })
}

const deleteArticle = async () => {
  if (confirm('정말 삭제하시겠습니까?')) {
    try {
      await axios({
        method: 'delete',
        url: `${store.API_URL}/api/board/articles/${route.params.id}/`,
        headers: {
          Authorization: `Token ${store.token}`
        }
      })
      router.push({ name: 'board' })
    } catch (err) {
      console.log(err)
    }
  }
}

const getImageUrl = (imagePath) => {
  return `${store.API_URL}${imagePath}`
}

const articleList = () => {
  router.push({ name: 'board'})
}

onMounted(() => {
  getArticle()
})
</script>

<style scoped>
.image-container {
  margin: 1rem 0;
}

.image-container img {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
}

.button-group {
  margin-top: 1rem;
}

.edit-btn, .delete-btn {
  padding: 0.5rem 1rem;
  margin-right: 0.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.edit-btn {
  background-color: #4CAF50;
  color: white;
  text-decoration: none;
}

.delete-btn {
  background-color: #f44336;
  color: white;
}
</style>