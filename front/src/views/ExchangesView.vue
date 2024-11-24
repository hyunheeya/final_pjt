<template>
    <div class="exchange-calculator">
      <h2>환율 계산기</h2>
      <div class="calculator-form">
        <!-- 날짜 선택 입력 추가 -->
        <div class="input-group">
          <input 
            type="date" 
            v-model="selectedDate"
            :max="today"
            @change="getExchangeRate"
          >
        </div>
  
        <div class="input-group">
          <select v-model="selectedCurrency" @change="getExchangeRate">
            <option value="USD">미국 달러</option>
            <option value="JPY">일본 엔</option>
            <option value="EUR">유로</option>
            <option value="CNY">중국 위안</option>
          </select>
          <input type="number" v-model="amount" @input="calculate">
          <span>{{ selectedCurrency }}</span>
        </div>
  
        <div class="result-group">
          <input type="text" :value="convertedAmount" readonly>
          <span>₩</span>
        </div>
        <p class="note">* 엔화, 인도네시아 루피아는 100 단위, 나머지는 모두 1 단위</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    name: 'ExchangeCalculator',
    data() {
      return {
        selectedCurrency: 'USD',
        selectedDate: new Date().toISOString().split('T')[0], // 오늘 날짜를 기본값으로
        today: new Date().toISOString().split('T')[0], // 최대 선택 가능 날짜
        amount: 1,
        exchangeRate: 0,
        convertedAmount: 0,
        error: null
      }
    },
    methods: {
      async getExchangeRate() {
    try {
        // 날짜가 없을 경우 오늘 날짜 사용
        if (!this.selectedDate) {
            this.selectedDate = new Date().toISOString().split('T')[0];
        }
        
        const formattedDate = this.selectedDate.replace(/-/g, '');
        console.log(`요청 정보: 통화=${this.selectedCurrency}, 날짜=${formattedDate}`);
        
        const response = await axios.get(
            `http://127.0.0.1:8000/api/exchanges/rates/${this.selectedCurrency}/`,
            {
                params: { 
                    searchdate: formattedDate 
                },
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            }
        );

        console.log('API 응답:', response.data);  // 디버깅용 로그 추가

        if (response.data && typeof response.data.rate === 'number') {
            this.exchangeRate = response.data.rate;
            this.calculate();
        } else {
            throw new Error('유효하지 않은 환율 데이터');
        }
    } catch (error) {
        console.error('API 오류:', error);
        this.exchangeRate = 0;
        alert(error.response?.data?.error || '환율 정보를 가져오는데 실패했습니다');
    }
},
      calculate() {
        if (!this.amount) {
          this.convertedAmount = 0;xxxxxxxxxxxx
          return;
        }
        
        if (this.selectedCurrency === 'JPY') {
          this.convertedAmount = (this.amount * this.exchangeRate / 100).toFixed(2);
        } else {
          this.convertedAmount = (this.amount * this.exchangeRate).toFixed(2);
        }
      }
    },
    mounted() {
      this.getExchangeRate();
    }
  }
  </script>
  
  <style scoped>
  .exchange-calculator {
    max-width: 500px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .calculator-form {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }
  
  .input-group, .result-group {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  select, input {
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
    min-width: 120px;
  }
  
  input[readonly] {
    background-color: #f5f5f5;
  }
  
  .note {
    font-size: 12px;
    color: #666;
    margin-top: 10px;
  }
  
  span {
    font-weight: bold;
    min-width: 30px;
  }

  .input-group input[type="date"] {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 10px;
}
  </style>