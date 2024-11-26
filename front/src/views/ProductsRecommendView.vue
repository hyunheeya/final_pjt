<template>
  <div class="wrapper">
    <div class="container text-center">
      <h1 class="display-4 mb-4 fw-bold">예적금 상품 추천</h1>
      <h5>나에게 맞는 금융 상품을 추천받아보세요!</h5>
      <div>
        <div class="image-container">
          <img :src="randomImage" alt="Random Character" class="img">
        </div>
        <RouterLink :to="{name: 'productsrecommendquiz'}">
          <button class="btn btn-warning btn-lg">시작하기</button>
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      images: [
        '/design/character/star1.png',
        '/design/character/star2.png',
        '/design/character/star3.png',
        '/design/character/star4.png',
        '/design/character/star5.png',
        '/design/character/star6.png',
        '/design/character/star7.png'
      ],
      randomImage: ''
    };
  },
  mounted() {
    this.setRandomImage();
  },
  methods: {
    setRandomImage() {
      const randomIndex = Math.floor(Math.random() * this.images.length);
      this.randomImage = this.images[randomIndex];
    }
  }
};
</script>

<style scoped>
/* 화면 전체를 감싸는 wrapper */
/* wrapper 스타일 수정 */
.wrapper {
  display: flex;
  justify-content: center; /* 컨텐츠 중앙 정렬 */
  align-items: center; /* 수직 가운데 정렬 */
  flex-direction: column; /* 세로 방향 정렬 */
  height: 80vh; /* 전체 높이 늘리기 */
  background-color: #fffbe6; /* 배경색 */
  padding: 20px; /* 위아래 여백 설정 */
  margin: 4% 0%; /* 외부 여백 제거 */
  overflow: hidden; /* 불필요한 스크롤 방지 */
}

/* container 수정 */
.container {
  text-align: center; /* 텍스트 중앙 정렬 */
  max-width: 900px; /* 컨테이너 최대 너비 확장 */
  width: 90%; /* 반응형 너비 */
  margin: 8% auto; /* 중앙 정렬 */
  padding: 10%; /* 내부 여백 */
}

/* h1 스타일 수정 */
h1 {
  font-size: 4rem; /* 제목 폰트 크기 약간 축소 */
  font-weight: 700; /* 폰트 굵게 설정 */
  margin-top: 10px; /* 상단 간격 줄이기 */
  margin-bottom: 20px; /* 아래 간격 설정 */
  line-height: 1.2; /* 줄 간격 조정 */
  word-break: keep-all; /* 단어 단위로 줄바꿈 방지 */
  white-space: nowrap; /* 줄바꿈 강제 방지 */
}

/* h5 스타일 수정 */
h5 {
  font-size: 1.5rem; /* 부제목 크기를 키움 */
  color: #555; /* 텍스트 색상 변경 */
  margin-bottom: 40px; /* 아래 여백 더 추가 */
}

/* 이미지 스타일 */
.img {
  max-width: 60%; /* 이미지 크기 확대 */
  height: auto; /* 비율 유지 */
  margin: 30px auto; /* 상하 여백 추가 및 가운데 정렬 */
}

/* 버튼 스타일 */
button {
  font-size: 1.5rem; /* 버튼 텍스트 크기 키움 */
  padding: 15px 30px; /* 버튼 크기 확대 */
  margin-top: 20px; /* 상단 간격 추가 */
  border-radius: 8px; /* 버튼 둥글게 */
}
</style>
