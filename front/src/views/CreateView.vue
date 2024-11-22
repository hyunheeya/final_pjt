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
const store = useCounterStore()
const router = useRouter()

const createArticle = function() {
  axios({
    method: 'post',
    url: `${store.API_URL}/api/articles/`,
    data: {
      title: title.value,
      content: content.value
    },
  })
  .then(() => {
    router.push({ name: 'boardarticle'})
  })
  .catch((err) => {
    console.log(err)
  })
}

</script>

<style scoped>

</style>