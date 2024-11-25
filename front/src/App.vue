<template>
  <div>
    <NavBar />
    <!-- 툴팁 버튼 -->
    <div class="tooltip-button">
      <button 
        class="btn btn-warning rounded-circle"
        ref="tooltipBtn"
        data-bs-toggle="tooltip"
        data-bs-placement="top"
        title="도움이 필요하세요?"
        @click="toggleChatbot"
      >
        <i class="bi bi-question-lg"></i>
      </button>
    </div>
    <!-- 챗봇 모달 -->
    <div class="chatbot-modal" :class="{ 'show': showChatbot }">
      <div class="chatbot-header">
        <h5>챗봇 상담</h5>
        <button class="btn-close" @click="toggleChatbot"></button>
      </div>
      <div class="chatbot-body">
        <ChatbotComponent />
      </div>
    </div>
  </div>

  <!-- 푸터 -->
  <footer class="footer">
  <div class="footer-container">
    <!-- 회사 정보 -->
    <div class="footer-company">
      <img src="/design/StarPot.png" alt="StarPot 로고" class="footer-logo" />
      <p>© 2024 StarPot. All Rights Reserved.</p>
      <p>주소: 서울특별시 강남구 테헤란로 123, 스타타워 12층</p>
    </div>

    <!-- 고객 지원 -->
    <div class="footer-support">
      <h4>고객 지원</h4>
      <ul>
        <li><a href="#">고객센터</a></li>
        <li><a href="#">FAQ</a></li>
        <li><a href="#">이용약관</a></li>
        <li><a href="#">개인정보처리방침</a></li>
      </ul>
    </div>

    <!-- 소셜 미디어 -->
    <div class="footer-social">
      <h4>소셜 미디어</h4>
      <div class="social-links">
        <a href="https://facebook.com" target="_blank">Facebook</a>
        <a href="https://twitter.com" target="_blank">Twitter</a>
        <a href="https://instagram.com" target="_blank">Instagram</a>
        <a href="https://youtube.com" target="_blank">YouTube</a>
      </div>
    </div>
  </div>
</footer>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import NavBar from '@/components/NavBar.vue'
import ChatbotComponent from '@/components/ChatbotView.vue'
import { Tooltip } from 'bootstrap'
const showChatbot = ref(false)
const tooltipBtn = ref(null)

onMounted(() => {
  // 툴팁 초기화
  new Tooltip(tooltipBtn.value)
})
const toggleChatbot = () => {
  showChatbot.value = !showChatbot.value
}
</script>

<style scoped>
.tooltip-button {
  position: fixed;
  bottom: 30px;
  right: 30px;
  z-index: 1000;
}
.tooltip-button button {
  width: 50px;
  height: 50px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.2);
}
.chatbot-modal {
  position: fixed;
  bottom: 100px;
  right: 30px;
  width: 40vw;
  height: 60vh;
  background: white;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.3);
  display: none;
  z-index: 1050;
}
.chatbot-modal.show {
  display: block;
}
.chatbot-header {
  padding: 15px;
  border-bottom: 1px solid #dee2e6;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.chatbot-body {
  height: calc(100% - 56px);
  padding: 5px;
  display: flex;
  flex-direction: column;
}
/* ChatbotComponent 내부 스타일 */
.chatbot-body :deep(.chat-container) {
  height: 100%;
  display: flex;
  flex-direction: column;
  margin: 0;
}
.chatbot-body :deep(.chat-messages) {
  width: 100%;
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  margin-bottom: 10px;
}
.chatbot-body :deep(.input-container) {
  padding: 10px;
  background: white;
  border-top: 1px solid #dee2e6;
}
.chatbot-body :deep(.input-container input) {
  width: calc(100% - 80px);
}


/* footer */
/* 페이지 컨테이너: Flexbox 설정 */
.page-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* 뷰포트 전체 높이 */
}

/* 헤더 스타일 */
.header {
  background-color: #f8f9fa;
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid #dee2e6;
}

.header nav a {
  margin: 0 10px;
  text-decoration: none;
  color: #007bff;
}

.header nav a:hover {
  color: #0056b3;
}

/* 본문 스타일 */
.main-content {
  flex: 1; /* 남는 공간을 차지 */
  padding: 20px;
  text-align: center;
}

/* Footer 스타일 */
.footer {
  background-color: #f8f9fa;
  margin: 300px 0px 0px 0px;
  padding: 20px;
  text-align: center;
  font-size: 14px;
  color: #343a40;
  border-top: 1px solid #dee2e6;
  /* margin-top: auto; 본문 내용이 짧을 때 Footer가 아래로 내려감 */
}

/* Footer 컨테이너 */
.footer-container {
  display: flex;
  flex-wrap: wrap; /* 반응형 지원 */
  justify-content: space-around; /* 균등 분배 */
  align-items: flex-start;
  max-width: 1200px;
  margin: 0 auto;
}

/* 회사 정보 */
.footer-company {
  flex: 1 1 300px;
  text-align: left;
  margin-bottom: 20px;
}

.footer-logo {
  width: 100px;
  margin-bottom: 10px;
}

.footer-company p {
  margin: 5px 0;
  font-size: 12px;
}

/* 고객 지원 */
.footer-support,
.footer-social {
  flex: 1 1 200px;
  margin-bottom: 20px;
  text-align: left;
}

.footer-support h4,
.footer-social h4 {
  font-size: 16px;
  margin-bottom: 10px;
  font-weight: bold;
}

.footer-support ul,
.footer-social .social-links {
  list-style: none;
  padding: 0;
}

.footer-support ul li a,
.footer-social .social-links a {
  text-decoration: none;
  color: #007bff;
  transition: color 0.3s ease;
}

.footer-support ul li a:hover,
.footer-social .social-links a:hover {
  color: #0056b3;
}
</style>