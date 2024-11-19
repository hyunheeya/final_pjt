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
      <div v-else>
        <input
          type="text"
          v-model="answers[currentQuestion.id]"
          @change="saveAnswer(currentQuestion.id, answers[currentQuestion.id])"
        />
      </div>
    </div>

    <!-- 추천 버튼 -->
    <button v-if="!currentQuestion && recommendations.length === 0" @click="submitAnswers">
      추천받기
    </button>

    <!-- 추천 결과 표시 -->
    <div v-if="recommendations.length > 0">
      <h2>추천 결과</h2>
      <ul>
        <li v-for="rec in recommendations" :key="rec.name">
          {{ rec.name }} - 금리: {{ rec.interest_rate }}%
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      // 질문 데이터
      questions: {
        main: [{ id: 1, text: "추천 받고 싶은 상품 유형이 어떤 것인가요?", options: ["예금", "적금"] }],
        deposit: [
          { id: 2, text: "어떤 가입 방식을 선호하시나요?", options: ["영업점", "인터넷", "스마트폰", "전화(텔레뱅킹)"] },
          { id: 3, text: "선호하는 저축 금리 유형을 선택해주세요.", options: ["단리", "복리"] },
          { id: 4, text: "선호하는 저축 기간을 선택해주세요.", options: ["6개월 이하", "6개월~1년", "1년 이상"] },
        ],
        savings: [
          { id: 2, text: "어떤 가입 방식을 선호하시나요?", options: ["영업점", "인터넷", "스마트폰", "전화(텔레뱅킹)"] },
          { id: 3, text: "선호하는 저축 금리 유형을 선택해주세요.", options: ["단리", "복리"] },
          { id: 4, text: "선호하는 저축 기간을 선택해주세요.", options: ["6개월 이하", "6개월~1년", "1년 이상"] },
        ],
      },
      answers: {}, // 답변 저장
      currentQuestion: null, // 현재 표시 중인 질문
      questionQueue: [], // 처리할 질문 목록
      recommendations: [], // 추천 결과 저장
    };
  },
  methods: {
    // 설문 시작
    startQuestionnaire() {
      this.questionQueue = [...this.questions.main];
      this.currentQuestion = this.questionQueue.shift();
    },
    // 답변 저장 및 다음 질문으로 이동
    saveAnswer(questionId, answer) {
      this.answers[questionId] = answer;

      // 첫 번째 질문의 답변에 따라 다음 질문 목록 설정
      if (questionId === 1) {
        const productType = answer === "예금" ? "deposit" : "savings";
        this.questionQueue = [...this.questions[productType]];
      }

      // 다음 질문 표시
      this.currentQuestion = this.questionQueue.shift();
    },
    // 추천 요청
    submitAnswers() {
      axios
        .post("http://localhost:8000/recommend/", this.answers)
        .then((response) => {
          if (response.data && response.data.recommendations) {
            this.recommendations = response.data.recommendations;
          } else {
            alert("추천 결과를 가져오는 데 실패했습니다.");
          }
        })
        .catch((error) => {
          console.error("추천 요청 에러:", error);
          alert("추천 요청 중 문제가 발생했습니다. 다시 시도해주세요.");
        });
    },
  },
  mounted() {
    this.startQuestionnaire();
  },
};
</script>

<style scoped>
/* 스타일을 여기에 추가하세요 */
</style>
