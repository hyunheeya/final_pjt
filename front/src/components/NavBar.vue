<template>
  <header>
    <nav class="navbar navbar-expand-lg bg-light">
    <div class="container-fluid">
      <!-- 로고 -->
      <router-link to="/">
        <img src="/design/logo/StarPot_logo_ai.png" alt="StarPot Logo" class="logo me-3" />
      </router-link>

      <!-- 토글 버튼 -->
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- 네비게이션 메뉴 -->
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <a class="nav-link" href="#" @click.prevent="navigateTo('home')">홈</a>
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
            <a class="nav-link" href="#" @click.prevent="navigateTo('board')">똑똑 게시판</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#" @click.prevent="navigateTo('exchanges')">환율 계산기</a>
          </li>
        </ul>

        <!-- 회원가입, 로그인 버튼 --> 
        <!-- 로그인 안 한 경우 -->
        <div class="d-flex" v-if="!isLogin">
          <p>로그인을 해주세요</p>
          <a class="btn btn-warning me-2" href="#" @click.prevent="navigateTo('signup')">회원가입</a>
          <a class="btn btn-outline-secondary" href="#" @click.prevent="navigateTo('login')">로그인</a>
        </div>

        <!-- 로그인 한 경우 -->
        <div class="d-flex" v-if="isLogin">
          <p>{{ username }}님 환영합니다!</p>
          <a class="btn btn-warning me-2" href="#" @click.prevent="navigateTo('profile')">마이페이지</a>
          <a class="btn btn-outline-secondary" href="#" @click.prevent="logOut">로그아웃</a>
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
import { computed,onMounted } from "vue";

const router = useRouter();
const store = useCounterStore();
const username = computed(() => store.userInfo?.username);
const isLogin = computed(() => store.isLogin);

// 네비게이션 
const navigateTo = (routeName) => {
  router.push({ name: routeName });
};

const logOut = () => {
  store.logOut(); // 스토어의 로그아웃 함수 호출
};

// onMounted에서 로그인 여부 확인 후 사용자 정보 요청
onMounted(async () => {
  if (store.isLogin) {
    try {
      await store.getUserInfo();
    } catch (error) {
      console.error("사용자 정보를 불러오는 데 실패했습니다:", error);
    }
  }
});
</script>


<style scoped>
  .navbar-nav .nav-link {
    margin-right: 15px; /* 메뉴 간격 설정 */
  }

  .logo {
  height: 100%; /* 네비게이션 바 높이에 맞게 */
  max-height: 50px; /* 최대 높이 제한 (선택 사항) */  
  object-fit: contain; /* 이미지 비율 유지 */
  }

  .d-flex p {
  margin: 0; /* p 태그의 기본 여백 제거 */
  padding: 5px
  }

</style>
