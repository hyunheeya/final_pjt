<template>
  <div class="profile">
    <h1 class="h1">프로필</h1>
        <!-- 탭 -->
        <div class="product-tabs">
      <button 
        @click="showComponent('mypage')" 
        :class="['tab-button', currentView === 'mypage' ? 'active' : '']"
      >
        프로필
      </button>
      <button 
        @click="showComponent('mylikelist')" 
        :class="['tab-button', currentView === 'mylikelist' ? 'active' : '']"
      >
        좋아요한 상품
      </button>
      <button 
        @click="showComponent('mycommentlist')" 
        :class="['tab-button', currentView === 'mycommentlist' ? 'active' : '']"
      >
        내가 쓴 댓글
      </button>

    </div>
        <!-- 컴포넌트 표시 영역 -->
      <div class="tab-content">
        <ProfileMyPage v-if="currentView === 'mypage'" />
        <ProfileMyLikeList v-if="currentView === 'mylikelist'" />
        <ProfileMyCommentList v-if="currentView === 'mycommentlist'" />
      </div>
  </div>
</template>

<script setup>
import { ref, onMounted} from 'vue';
import ProfileMyPage from '@/components/ProfileMyPage.vue';
import ProfileMyLikeList from '@/components/ProfileMyLikeList.vue';
import ProfileMyCommentList from '@/components/ProfileMyCommentList.vue';



const currentView = ref('mypage')

const showComponent = (view) => {
  currentView.value = view;
};

// 첫 화면은 마이페이지 보여주기
onMounted(() => {
  showComponent('mypage');
});
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.h1{
  margin: 0;
  padding: 24px;
}

.title {
  font-size: 1.75rem;
  margin-bottom: 2rem;
}

.product-tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid #e9ecef;
}

.tab-button {
  padding: 0.75rem 2rem;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 1rem;
}

.tab-button.active {
  color: #007bff;
  border-bottom: 2px solid #007bff;
}

</style>