<template>
  <div class="container mt-4">
    <div v-if="isLoading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">로딩 중...</span>
      </div>
    </div>
    <div v-else>
      <div v-if="articles && articles.length > 0" class="list-group">
        <RouterLink 
          v-for="article in articles" 
          :key="article.id"
          :to="{ name: 'boardarticledetail', params: { id: article.id }}"
          class="list-group-item list-group-item-action"
        >
          <div class="d-flex w-100 justify-content-between">
            <h5 class="mb-1">{{ article.title }}</h5>
            <small>{{ formatDate(article.created_at) }}</small>
          </div>
        </RouterLink>
      </div>
      <div v-else class="alert alert-warning" role="alert">
        게시글이 없습니다.
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'  // import 추가

defineProps({
  articles: {
    type: Array,
    required: true,
    default: () => []
  },
  isLoading: {
    type: Boolean,
    required: true,
    default: false
  },
  formatDate: {
    type: Function,
    required: true
  }
})
</script>

<style scoped>

</style>