<template>
  <div class="container mt-5">
    <div class="card shadow-sm">
      <!-- 게시글 헤더 -->
      <div class="card-header bg-success bg-gradient text-white py-3">
        <h3 class="card-title mb-0">{{ article?.title }}</h3>
        <small class="text-white-50">{{ formatDate(article?.created_at) }}</small>
      </div>

      <!-- 게시글 본문 -->
      <div class="card-body">
        <!-- 마크다운 렌더링 영역 -->
        <div class="content-area mb-4">
          <VueMarkdown 
            :markdown="article?.content"
            :custom-attrs="markdownAttrs"
          >
            <!-- 코드 블록 커스텀 렌더링 -->
            <template #code="{ children, language, inline }">
              <code v-if="inline" class="inline-code">
                <Component :is="children" />
              </code>
              <pre v-else class="code-block" :class="language">
                <code :class="language">
                  <Component :is="children" />
                </code>
              </pre>
            </template>
          </VueMarkdown>
        </div>

        <!-- 이미지 영역 -->
        <div v-if="article?.image" class="image-area mb-4">
          <img :src="getImageUrl(article.image)" 
               :alt="article.title"
               class="img-fluid rounded">
        </div>
      </div>

      <!-- 버튼 그룹 -->
      <div class="card-footer bg-white">
        <div class="d-flex justify-content-between align-items-center">
          <!-- 목록 버튼 -->
          <button @click="articleList" 
                  class="btn btn-outline-success">
            <i class="fas fa-list me-1"></i> 목록
          </button>

          <!-- 관리자 전용 버튼 -->
          <div v-if="isAdmin" class="admin-buttons">
            <RouterLink 
              :to="{ name: 'edit', params: { id: article?.id }}" 
              class="btn btn-warning me-2">
              <i class="fas fa-edit me-1"></i> 수정
            </RouterLink>
            <button @click="deleteArticle" 
                    class="btn btn-danger">
              <i class="fas fa-trash me-1"></i> 삭제
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useCounterStore } from '@/stores/counter'
import VueMarkdown from '@crazydos/vue-markdown'

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

// 마크다운 커스텀 속성 설정
const markdownAttrs = {
  h1: { class: ['text-2xl', 'font-bold', 'my-4'] },
  h2: { class: ['text-xl', 'font-bold', 'my-3'] },
  h3: { class: ['text-lg', 'font-bold', 'my-2'] },
  p: { class: ['my-2'] },
  a: { 
    class: ['text-blue-500', 'hover:underline'],
    target: '_blank',
    rel: 'noopener noreferrer'
  },
  ul: { class: ['list-disc', 'ml-4', 'my-2'] },
  ol: { class: ['list-decimal', 'ml-4', 'my-2'] },
  blockquote: { class: ['border-l-4', 'border-gray-300', 'pl-4', 'my-2'] },
  table: { class: ['table', 'table-bordered', 'my-3'] }
}

onMounted(() => {
  getArticle()
})
</script>

<style scoped>
.card {
  border: none;
  border-radius: 10px;
}

.card-header {
  border-top-left-radius: 10px !important;
  border-top-right-radius: 10px !important;
}

.content-area {
  min-height: 200px;
  line-height: 1.8;
  white-space: pre-wrap;
}

.image-area img {
  max-height: 500px;
  object-fit: contain;
}

.btn {
  padding: 0.5rem 1.5rem;
  border-radius: 5px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn:hover {
  transform: translateY(-2px);
}

.admin-buttons .btn {
  min-width: 100px;
}

@media (max-width: 768px) {
  .card-footer .d-flex {
    flex-direction: column;
    gap: 1rem;
  }
  
  .admin-buttons {
    width: 100%;
    display: flex;
    justify-content: flex-end;
  }
}

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

.content-area :deep(.inline-code) {
  background-color: #f3f4f6;
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  font-family: monospace;
}

.content-area :deep(.code-block) {
  background-color: #1f2937;
  color: #f3f4f6;
  padding: 1rem;
  border-radius: 6px;
  margin: 1rem 0;
  overflow-x: auto;
}

.content-area :deep(table) {
  width: 100%;
  border-collapse: collapse;
}

.content-area :deep(th),
.content-area :deep(td) {
  border: 1px solid #e5e7eb;
  padding: 0.5rem;
}

.content-area :deep(blockquote) {
  color: #4b5563;
  font-style: italic;
}
</style>