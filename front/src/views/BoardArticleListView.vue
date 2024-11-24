<template>
  <div>
    <!-- <BoardArticleDetailView :formatDate="formatDate" /> -->
    <div v-if="articles && articles.length">
      <div v-for="article in articles" :key="article.id">
        <RouterLink :to="{ name: 'boardarticledetail', params: { id: article.id }}">
          <h3>{{ article.title }}</h3>
          <span>{{ formatDate(article.created_at) }}</span>
          <hr>
        </RouterLink>
      </div>
    </div>
    <div v-else>
      <p>게시글이 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
// import BoardArticleDetailView from '@/components/BoardArticleDetailView.vue'
defineProps({
  articles: {
    type: Array,
    required: true
  },
  formatDate: {
    type: Function,
    required: true
  }
})
</script>

<style scoped>

</style>