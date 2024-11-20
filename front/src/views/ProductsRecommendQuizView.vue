<template>
  <div>
    <h1>금융 상품 추천</h1>
    <!-- 현재 질문 표시 -->
    <div v-if="currentQuestion">
      <p>{{ currentQuestion.text }}</p>
      <div v-if="currentQuestion.options && currentQuestion.options.length > 0">
        <button
          v-for="option in currentQuestion.options"
          :key="option"
          @click="saveAnswer(currentQuestion.id, option)"
        >
          {{ option }}
        </button>
      </div>
      <div v-else-if="currentQuestion.type === 'number'">
        <!-- 숫자 입력 -->
        <input
          type="number"
          v-model="answers[currentQuestion.id]"
          @keyup.enter="saveAnswer(currentQuestion.id, answers[currentQuestion.id])"
          :placeholder="currentQuestion.placeholder"
        />
        <button
          @click="saveAnswer(currentQuestion.id, answers[currentQuestion.id])"
        >
          다음
        </button>
      </div>

      <div v-else>
        <!-- 텍스트 입력 -->
        <input
          type="text"
          v-model="answers[currentQuestion.id]"
          @click="saveAnswer(currentQuestion.id, answers[currentQuestion.id])"
        />
      </div>
    </div>

    <!-- 추천 버튼 -->
    <button
      v-if="!currentQuestion && recommendations.length === 0"
      @click="submitAnswers"
    >
      추천받기
    </button>
  </div>
</template>

<script>
import { useCounterStore } from "@/stores/counter"
import axios from "axios"

export default {
  data() {
    return {
      questions: {
        main: [
          { id: 1, text: "추천 받고 싶은 상품 유형이 어떤 것인가요?", options: ["예금", "적금"] },
        ],
        deposit: [
          { id: 2, text: "어떤 가입 방식을 선호하시나요?", options: ["영업점", "인터넷", "스마트폰", "전화(텔레뱅킹)"] },
          { id: 3, text: "선호하는 저축 금리 유형을 선택해주세요.", options: ["단리", "복리"] },
          { id: 4, text: "선호하는 저축 기간을 선택해주세요.", options: ["3개월", "6개월", "1년", "2년", "3년"] },
          { id: 5, text: "귀하의 나이는 몇 살인가요?", type: "number", placeholder: "나이를 입력해주세요" },
          { id: 6, text: "예적금 가능한 금액은 얼마인가요?", type: "number", placeholder: "금액을 입력해주세요" },
        ],
        savings: [
          { id: 2, text: "어떤 가입 방식을 선호하시나요?", options: ["영업점", "인터넷", "스마트폰", "전화(텔레뱅킹)"] },
          { id: 3, text: "선호하는 저축 유형을 선택해주세요.", options: ["자유적립식", "정액적립식"] },
          { id: 4, text: "선호하는 저축 금리 유형을 선택해주세요.", options: ["단리", "복리"] },
          { id: 5, text: "선호하는 저축 기간을 선택해주세요.", options: ["3개월", "6개월", "1년", "2년", "3년"] },
          { id: 6, text: "귀하의 나이는 몇 살인가요?", type: "number", placeholder: "나이를 입력해주세요" },
          { id: 7, text: "예적금 가능한 금액은 얼마인가요?", type: "number", placeholder: "금액을 입력해주세요" },
        ],
      },
      answers: {}, // 답변 저장
      currentQuestion: null, // 현재 질문
      questionQueue: [], // 처리할 질문 목록
      recommendations: [], // 추천 결과
    };
  },
  computed: {
  token() {
    return useCounterStore().token || localStorage.getItem("token"); // Pinia 또는 로컬 스토리지에서 토큰 가져오기
  },
},

  methods: {
  startQuestionnaire() {
    // 질문 큐 초기화 (5번과 6번을 마지막에 추가)
    this.questionQueue = [...this.questions.main];
    this.currentQuestion = this.questionQueue.shift();
  },
  saveAnswer(questionId, answer) {
    this.answers[questionId] = answer;

    // 다음 질문 설정
    if (questionId === 1) {
      const productType = answer === "예금" ? "deposit" : "savings";
      this.questionQueue = [...this.questions[productType], ...this.questions.main.slice(1)]; // 5, 6번 추가
    }

    this.currentQuestion = this.questionQueue.shift();
  },
  submitAnswers() {
  const token = this.token || localStorage.getItem("token"); // 토큰 확인

  if (!token) {
    console.error("Authentication token is missing.");
    return;
  }

  console.log("Token:", token); // 디버깅용: 토큰 값 출력

  const params = new URLSearchParams();
  Object.keys(this.answers).forEach((key) => {
    params.append(key, this.answers[key]);
  });

  axios
    .post("http://127.0.0.1:8000/recommend/", params, {
      headers: {
        Authorization: `Token ${token}`,
        "Content-Type": "application/x-www-form-urlencoded",
      },
    })
    .then((response) => {
      if (response.data && response.data.recommendations) {
        this.recommendations = response.data.recommendations;
        this.$router.push({
          name: "productsrecommendresult",
          query: { results: JSON.stringify(this.recommendations) },
        });
      } else {
        console.error("Invalid response format:", response.data);
        // 사용자에게 오류 메시지 표시
      }
    })
    .catch((error) => {
      console.error("추천 요청 중 에러 발생:", error);
      if (error.response) {
        console.error("Response status:", error.response.status);
        console.error("Response data:", error.response.data);
        // 사용자에게 오류 메시지 표시
      }
    });
}




  },

  mounted() {
    this.startQuestionnaire();
  },
};
</script>

<style scoped>
/* 스타일을 여기에 추가하세요 */

</style>

