<template>
  <div class="container mt-5">
    <h1 class="mb-4">게시글 작성</h1>
    <form @submit.prevent="createArticle">
      <div class="mb-3">
        <label for="title" class="form-label">제목:</label>
        <input type="text" class="form-control" id="title" v-model.trim="title">
      </div>
      <div class="mb-3">
        <label for="content" class="form-label">내용:</label>
        <textarea class="form-control" id="content" rows="5" v-model.trim="content"></textarea>
      </div>
      <div class="mb-3">
        <label for="image" class="form-label">이미지:</label>
        <input 
          type="file" 
          class="form-control" 
          id="image" 
          @change="handleImageChange"
          accept="image/*"
        >
      </div>
      <button type="submit" class="btn btn-primary">게시글 작성</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'

const title = ref(null)
const content = ref(null)
const image = ref(null)
const store = useCounterStore()
const router = useRouter()

const handleImageChange = (event) => {
  image.value = event.target.files[0]
}

const createArticle = function() {
  const formData = new FormData()
  formData.append('title', title.value)
  formData.append('content', content.value)
  if (image.value) {
    formData.append('image', image.value)
  }

  axios({
    method: 'post',
    url: `${store.API_URL}/api/board/articles/`,
    data: formData,
    headers: {
      'Authorization': `Token ${store.token}`,
      'Content-Type': 'multipart/form-data'
    }
  })
  .then((res) => {
    router.push({ name: 'boardarticledetail', params: { id: res.data.id }})
  })
  .catch((err) => {
    console.log(err)
  })
}
</script>