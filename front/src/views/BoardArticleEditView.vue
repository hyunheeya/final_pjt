<template>
    <div>
      <h2>게시글 수정</h2>
      <form @submit.prevent="updateArticle">
        <div class="form-group">
          <label for="title">제목:</label>
          <input 
            type="text" 
            id="title" 
            v-model="formData.title" 
            required
          >
        </div>
        <div class="form-group">
          <label for="content">내용:</label>
          <textarea 
            id="content" 
            v-model="formData.content" 
            required
          ></textarea>
        </div>
        <div class="form-group">
          <label for="image">이미지:</label>
          <input 
            type="file" 
            id="image" 
            @change="handleImageChange"
            accept="image/*"
          >
          <!-- 현재 이미지 미리보기 -->
          <div v-if="currentImage" class="image-preview">
            <img :src="currentImage" alt="현재 이미지">
          </div>
        </div>
        <div class="button-group">
          <button type="submit">수정</button>
          <button type="button" @click="goBack">취소</button>
        </div>
      </form>
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
  
  const updateArticle = async () => {
    try {
      const form = new FormData()
      form.append('title', formData.value.title)
      form.append('content', formData.value.content)
      
      // 새 이미지가 선택된 경우에만 이미지 추가
      if (formData.value.image instanceof File) {
        form.append('image', formData.value.image)
      }
  
      const response = await axios({
        method: 'put',
        url: `${store.API_URL}/api/board/articles/${route.params.id}/`,
        data: form,
        headers: {
          'Authorization': `Token ${store.token}`,
          // Content-Type 헤더 제거 (자동으로 설정됨)
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
  .image-preview {
    margin-top: 1rem;
    max-width: 300px;
  }
  
  .image-preview img {
    width: 100%;
    height: auto;
    border-radius: 4px;
  }
  
  .form-group {
    margin-bottom: 1rem;
  }
  
  .form-group label {
    display: block;
    margin-bottom: 0.5rem;
  }
  
  .form-group input,
  .form-group textarea {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  .form-group textarea {
    height: 150px;
  }
  
  .button-group {
    margin-top: 1rem;
  }
  
  .submit-btn,
  .cancel-btn {
    padding: 0.5rem 1rem;
    margin-right: 0.5rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .submit-btn {
    background-color: #4CAF50;
    color: white;
  }
  
  .cancel-btn {
    background-color: #f44336;
    color: white;
  }
  </style>