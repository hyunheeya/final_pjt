<template>
  <div>
    <NavBar />
    <!-- 툴팁 버튼 -->
    <div class="tooltip-button">
      <button 
        class="btn btn-primary rounded-circle"
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
</style>