<template>
  <div>
    <h1>게시글 작성</h1>
    <form @submit.prevent="createArticle">
      <div>
        <label for="title">제목 : </label>
        <input type="text" id="title" v-model.trim="title">
      </div>
      <div>
        <label for="content">내용 : </label>
        <textarea id="content" v-model.trim="content"></textarea>
      </div>
      <div>
        <label for="image">이미지 : </label>
        <input 
          type="file" 
          id="image" 
          @change="handleImageChange"
          accept="image/*"
        >
      </div>
      <input type="submit">
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
  axios({
    method: 'post',
    url: `${store.API_URL}/api/board/articles/`,
    data: {
      title: title.value,
      content: content.value,
      image: image.value
    },
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

<style scoped>

</style>