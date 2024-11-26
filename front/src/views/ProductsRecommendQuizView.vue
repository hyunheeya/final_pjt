<template>
  <div class="container mt-5">
    <h1 class="text-center mb-4">금융 상품 추천</h1>
    <!-- 현재 질문 표시 -->
    <div v-if="currentQuestion" class="card p-4 shadow-sm">
      <p class="lead text-center mb-4">{{ currentQuestion.text }}</p>
      <!-- 선택형 옵션 -->
      <div v-if="currentQuestion.options && currentQuestion.options.length > 0" class="d-flex justify-content-center flex-wrap">
        <button
          v-for="option in currentQuestion.options"
          :key="option"
          @click="saveAnswer(currentQuestion.id, option)"
          class="btn btn-outline-success m-2"
        >
          {{ option }}
        </button>
      </div>
      <!-- 숫자 입력 -->
      <div v-else="currentQuestion.type === 'number'" class="text-center">
        <input
          type="text"
          id="ageInput"
          v-model="answers[currentQuestion.id]"
          @input="validateNumberInput"
          :placeholder="currentQuestion.placeholder"
          class="form-control my-3"
        />
        <button
          @click="saveAnswer(currentQuestion.id, answers[currentQuestion.id])"
          class="btn btn-success"
        >
          다음
        </button>
      </div>
    </div>

    <!-- 추천 버튼 -->
    <div v-if="!currentQuestion && recommendations.length === 0" class="text-center mt-4">
      <h5>당신에게 맞는 금융 상품을 확인해볼까요?</h5>
      <img class="img" src="/design/logo/pot.png" alt="pot"><br>
      <button
        @click="submitAnswers"
        class="btn btn-warning btn-lg"
      >
        추천받기
      </button>
    </div>
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
          { id: 5, text: "귀하의 나이는 몇 살인가요? (숫자만 입력해 주세요.)", type: "number", placeholder: "나이를 입력해주세요" },
          { id: 6, text: "예금 가능한 금액은 얼마인가요? (단위: 원)", type: "number", placeholder: "금액을 입력해주세요" },
        ],
        savings: [
          { id: 2, text: "어떤 가입 방식을 선호하시나요?", options: ["영업점", "인터넷", "스마트폰", "전화(텔레뱅킹)"] },
          { id: 3, text: "선호하는 저축 금리 유형을 선택해주세요.", options: ["단리", "복리"] },
          { id: 4, text: "선호하는 저축 기간을 선택해주세요.", options: ["3개월", "6개월", "1년", "2년", "3년"] },
          { id: 5, text: "귀하의 나이는 몇 살인가요? (숫자만 입력해 주세요.)", type: "number", placeholder: "나이를 입력해주세요" },
          { id: 6, text: "적금 가능한 금액은 얼마인가요? (단위: 원)", type: "number", placeholder: "금액을 입력해주세요" },
          { id: 7, text: "선호하는 저축 유형을 선택해주세요.", options: ["자유적립식", "정액적립식"] },
        ],
      },
      answers: {}, // 답변 저장
      currentQuestion: null, // 현재 질문
      questionQueue: [], // 처리할 질문 목록
      recommendations: [], // 추천 결과
      ageWarning: '', // 나이 입력 경고 메시지
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
    // 입력값이 숫자인 경우 처리
    if (this.currentQuestion.type === 'number') {
      if ((questionId === 5 || questionId === 6) && (answer === '' || isNaN(answer))) {
        alert('숫자를 입력해주세요.');
        return; // 함수 실행 중단
      }
      const numericAnswer = parseInt(answer, 10)
      this.answers[questionId] = numericAnswer // 숫자 값 저장
    } else {
        // 일반 텍스트 또는 옵션 타입 질문 처리
        this.answers[questionId] = answer;
    }

    // 다음 질문 설정
    if (questionId === 1) {
      const productType = answer === "예금" ? "deposit" : "savings"
      this.questionQueue = [...this.questions[productType], ...this.questions.main.slice(1)]; // 5, 6번 추가
    }

    this.currentQuestion = this.questionQueue.shift();
  },
  validateNumberInput(event) {
    const input = event.target;
    const originalValue = input.value;
    const numericValue = originalValue.replace(/[^0-9]/g, '');
    
    // 문자가 입력되었을 때 한 번만 alert를 표시
    if (numericValue !== originalValue) {
        input.value = numericValue; // 숫자가 아닌 문자를 제거
        alert('숫자만 입력해주세요.');
        return;
    }

    if (this.currentQuestion.id === 5) {
        if (numericValue !== '') {
            const age = parseInt(numericValue, 10);
            if (age > 150) {
                input.value = '';
                alert('최대 나이는 150세입니다.');
            } else {
                this.answers[this.currentQuestion.id] = numericValue;
            }
        }
    } else { // currentQuestion.id === 6
        if (numericValue !== '') {
            this.answers[this.currentQuestion.id] = numericValue;
        }
    }
},
  submitAnswers() {
  const token = this.token || localStorage.getItem("token"); // 토큰 확인

  if (!token) {
    console.error("Authentication token is missing.");
    return;
  }

  const params = new URLSearchParams();
  Object.keys(this.answers).forEach((key) => {
    params.append(key, this.answers[key]);
  });

  axios
    .post("http://127.0.0.1:8000/api/recommend/recommend_products/", params, {
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
    })
}},

  mounted() {
    this.startQuestionnaire()
  },
}


</script>

<style scoped>
.container {
  display: flex; /* Flexbox 레이아웃 사용 */
  flex-direction: column; /* 세로 방향 정렬 */
  justify-content: start; /* 세로 가운데 정렬 */
  align-items: center; /* 수평 가운데 정렬 */
  min-height: 100vh; /* 화면 전체 높이를 기준으로 중앙 정렬 */
  text-align: center;
  padding: 0;
}
.text-center{
  padding: 0%;
}
.card {
  max-width: 800px; /* 카드의 최대 너비를 기존보다 넓게 설정 */
  width: 90%; /* 반응형 크기 설정 */
  text-align: center;
  margin: 4% auto; /* 수평 가운데 정렬 */
  padding: 40px; /* 내부 여백을 늘려서 더 커보이게 */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15); /* 그림자 강도를 조금 더 추가 */
  border-radius: 12px; /* 모서리를 더 둥글게 */
  background-color: #ffffff; /* 배경색 유지 */
}

  button {
    min-width: 120px;
  }

  img{
    width: 60%;
    padding: 40px;
  }
</style>