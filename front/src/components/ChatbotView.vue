<template>
  <div class="chat-container">
    <div class="chat-messages">
      <div v-for="(message, index) in messages" 
           :key="index" 
           :class="['message', message.type]">
        <div v-if="message.type === 'bot'" 
             v-html="formatMarkdown(message.content)" 
             class="markdown-content">
        </div>
        <div v-else>
          {{ message.content }}
        </div>
      </div>
    </div>
    
    <div class="input-container">
      <input v-model="userInput" 
             @keyup.enter="sendMessage" 
             placeholder="메시지를 입력하세요"
             :disabled="isLoading">
      <button @click="sendMessage" 
              :disabled="isLoading">전송</button>
    </div>
  </div>
</template>

<script>
import OpenAI from 'openai'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

export default {
  data() {
    return {
      messages: [],
      userInput: '',
      isLoading: false,
      openai: null,
      systemMessage: {
        role: "system",
        content: `당신은 친절하고 전문적인 금융 어시스턴트입니다. 
        다음 규칙을 따라 답변해주세요:
        1. 마크다운을 활용하여 시각적으로 보기 쉽게 답변
        2. 금융 외 주제는 '금융 관련 질문만 답변 가능합니다'라고 안내
        3. 초보자를 위한 쉬운 용어 사용
        4. ## 제목, **강조**, * 목록 등 마크다운 문법 적극 활용
        5. 예금, 적금 추천 시 핵심 정보만 간단히 제공`
      }
    }
  },
  created() {
    const apiKey = import.meta.env.VITE_OPENAI_API_KEY
    if (!apiKey) {
      console.error('API 키가 설정되지 않았습니다.')
      return
    }
    
    this.openai = new OpenAI({
      apiKey: apiKey,
      dangerouslyAllowBrowser: true
    })
    
    // 초기 메시지 설정
    this.messages.push({
      type: 'bot',
      content: '안녕하세요! 무엇을 도와드릴까요?'
    })
  },
  methods: {
    formatMarkdown(content) {
      return DOMPurify.sanitize(marked(content))
    },
    async sendMessage() {
      if (!this.userInput.trim() || this.isLoading) return
      
      const userMessage = this.userInput.trim()
      this.userInput = ''
      this.isLoading = true
      
      this.messages.push({
        type: 'user',
        content: userMessage
      })
      
      try {
        const response = await this.openai.chat.completions.create({
          model: "gpt-3.5-turbo",
          messages: [
            this.systemMessage,
            ...this.messages.map(msg => ({
              role: msg.type === 'user' ? 'user' : 'assistant',
              content: msg.content
            }))
          ],
          temperature: 0.7,
          max_tokens: 500
        })
        
        this.messages.push({
          type: 'bot',
          content: response.choices[0].message.content
        })
      } catch (error) {
        console.error('API 오류:', error)
        this.messages.push({
          type: 'error',
          content: '메시지 전송 중 오류가 발생했습니다.'
        })
      } finally { 
        this.isLoading = false
      }
    }
  }
}
</script>

<style scoped>
.chat-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.chat-messages {
  height: 500px;
  overflow-y: auto;
  border: 1px solid #ddd;
  padding: 20px;
  margin-bottom: 20px;
}

.message {
  margin: 10px 0;
  padding: 10px;
  border-radius: 8px;
}

.user {
  background-color: #e3f2fd;
  margin-left: 20%;
}

.bot {
  background-color: #f5f5f5;
  margin-right: 20%;
}

.error {
  background-color: #ffebee;
  text-align: center;
}

.input-container {
  display: flex;
  gap: 10px;
}

input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

button {
  padding: 10px 20px;
  background-color: #2196f3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled,
input:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.markdown-content :deep(h2) {
  font-size: 1.5em;
  margin: 1em 0;
  color: #1976d2;
}

.markdown-content :deep(strong) {
  font-weight: 600;
  color: #333;
}

.markdown-content :deep(ul) {
  list-style-type: disc;
  padding-left: 1.5em;
  margin: 1em 0;
}

.markdown-content :deep(code) {
  background-color: #f5f5f5;
  padding: 0.2em 0.4em;
  border-radius: 3px;
}

.markdown-content :deep(blockquote) {
  border-left: 4px solid #1976d2;
  margin: 1em 0;
  padding: 0.5em 1em;
  background-color: #f5f5f5;
}
</style>