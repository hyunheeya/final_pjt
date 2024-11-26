<template>
  <div class="container mt-5">
    <div class="card shadow-sm">
      <!-- 게시글 헤더 -->
      <div class="card-header bg-success bg-gradient text-white py-3">
        <h3 class="card-title mb-0">게시글 수정</h3>
      </div>

      <!-- 입력 폼 영역 -->
      <div class="card-body p-4">
        <form @submit.prevent="updateArticle">
          <div class="mb-3">
            <label for="title" class="form-label">제목</label>
            <input 
              type="text" 
              id="title"
              v-model="formData.title" 
              class="form-control"
              placeholder="제목을 입력하세요"
              required
            >
          </div>

          <div class="mb-3">
            <label for="content" class="form-label">내용</label>
            <textarea 
              id="content"
              v-model="formData.content" 
              class="form-control content-area"
              rows="15"
              placeholder="내용을 입력하세요"
              required
            ></textarea>
            <small class="text-muted">마크다운 문법을 지원합니다.</small>
          </div>

          <div class="mb-4">
            <label for="image" class="form-label">이미지</label>
            <input 
              type="file" 
              id="image"
              class="form-control" 
              accept="image/*"
              @change="handleImageChange"
            >
            <!-- 현재 이미지 미리보기 -->
            <div v-if="currentImage" class="image-preview mt-3">
              <img :src="currentImage" alt="현재 이미지" class="img-fluid rounded">
            </div>
            <div>
              <button type="button" @click="imageDelete" class="btn-image-delete btn-secondary">이미지 삭제</button>
            </div>
          </div>

          <!-- 버튼 그룹 -->
          <div class="d-flex justify-content-end gap-2">
            <button type="submit" class="btn btn-warning">
              <i class="fas fa-check me-1"></i>수정하기
            </button>
            <button type="button" @click="goBack" class="btn btn-secondary">
              <i class="fas fa-times me-1"></i>취소
            </button>
          </div>
        </form>
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
const currentImage = ref(null)

const formData = ref({
  title: '',
  content: '',
  image: null
})

const handleImageChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    formData.value.image = file
    currentImage.value = URL.createObjectURL(file)
  }
}

const getArticle = async () => {
  try {
    const response = await axios({
      method: 'get',
      url: `${store.API_URL}/api/board/articles/${route.params.id}/`,
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
    formData.value = {
      title: response.data.title,
      content: response.data.content,
      image: null // 기존 이미지는 별도로 관리
    }
    if (response.data.image) {
      currentImage.value = `${store.API_URL}${response.data.image}`
    }
  } catch (err) {
    console.log(err)
  }
}

const imageDelete = function() {
  formData.value.image = null
  currentImage.value = null
  // 이미지가 삭제되었음을 나타내는 플래그 추가
  formData.value.imageDeleted = true
  
  // 파일 입력 초기화
  const fileInput = document.getElementById('image')
  if (fileInput) {
    fileInput.value = ''
  }
}

const updateArticle = async () => {
  try {
    const form = new FormData()
    form.append('title', formData.value.title)
    form.append('content', formData.value.content)
    
    // 이미지 삭제 플래그가 있는 경우
    if (formData.value.imageDeleted) {
      form.append('image', '') // 빈 문자열을 보내 이미지 삭제 표시
    } 
    // 새 이미지가 있는 경우
    else if (formData.value.image instanceof File) {
      form.append('image', formData.value.image)
    }

    const response = await axios({
      method: 'put',
      url: `${store.API_URL}/api/board/articles/${route.params.id}/`,
      data: form,
      headers: {
        'Authorization': `Token ${store.token}`
      }
    })
    
    router.push({ 
      name: 'boardarticledetail', 
      params: { id: route.params.id }
    })
  } catch (err) {
    console.log(err)
  }
}

const goBack = function() {
  router.push({ 
      name: 'boardarticledetail', 
      params: { id: route.params.id }
    })
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
  resize: vertical;
}

.form-control:focus {
  border-color: #198754;
  box-shadow: 0 0 0 0.25rem rgba(25, 135, 84, 0.25);
}

.image-preview {
  max-width: 300px;
}

.image-preview img {
  width: 100%;
  height: auto;
  border-radius: 4px;
}

.btn {
  padding: 0.5rem 1.5rem;
  border-radius: 5px;
  font-weight: 500;
  transition: all 0.3s ease;
  width: 100%;
}

.btn:hover {
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .d-flex {
    flex-direction: column;
    gap: 1rem;
  }
  
  .btn-image-delete {
    padding: 0.5rem 1.5rem;
    border-radius: 5px;
    font-weight: 500;
    transition: all 0.3s ease;
  }

  .btn-image-delete:hover {
  transform: translateY(-2px);
}

}
</style>