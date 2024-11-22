<template>
  <header>
    <nav class="navbar navbar-expand-lg bg-light">
    <div class="container-fluid">
      <!-- 로고 -->
      <a class="navbar-brand" href="#">로고</a>

      <!-- 토글 버튼 -->
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- 네비게이션 메뉴 -->
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="#" @click.prevent="navigateTo('home')">홈</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#" @click.prevent="navigateTo('productsrecommend')">예적금 상품 추천</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#" @click.prevent="navigateTo('productslist')">예적금 상품 전체 리스트</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#" @click.prevent="navigateTo('bankmap')">주변 은행 검색</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#" @click.prevent="navigateTo('board')">톡톡 게시판</a>
          </li>
        </ul>
        <!-- 회원가입, 로그인 버튼 -->
         
        <!-- 로그인 안 한 경우 -->
        <div class="d-flex" v-if="!isLogin">
          <a class="btn btn-outline-primary me-2" href="#" @click.prevent="navigateTo('signup')">회원가입</a>
          <a class="btn btn-outline-secondary" href="#" @click.prevent="navigateTo('login')">로그인</a>
        </div>

        <!-- 로그인 한 경우 -->
        <div class="d-flex" v-if="isLogin">
          <a class="btn btn-outline-primary me-2" href="#" @click.prevent="navigateTo('profile')">마이페이지</a>
          <a class="btn btn-outline-secondary" href="#" @click.prevent="navigateTo('logOut')">로그아웃</a>
        </div>
      </div>
    </div>
  </nav>
  </header>

  <RouterView />
</template>

<script setup>
import { useRouter } from "vue-router";
import { useCounterStore } from "@/stores/counter";
import { computed } from "vue";

const router = useRouter();
const store = useCounterStore();
const isLogin = computed(() => store.isLogin);
const logOut = () => {
  store.logOut();
  router.push({ name: "home" }); // 로그아웃 후 홈으로 이동
};

// 네비게이션 함수
const navigateTo = (routeName) => {
  router.push({ name: routeName });
};

</script>


<style scoped>
  .navbar-nav .nav-link {
    margin-right: 15px; /* 메뉴 간격 설정 */
  }
</style>