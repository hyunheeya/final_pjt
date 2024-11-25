<template>
  <div class="main-container">
    <div id="carouselExampleCaptions" class="carousel slide" data-bs-ride="carousel">
      <!-- 캐러셀 인디케이터 -->
      <div class="carousel-indicators">
        <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
        <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="1" aria-label="Slide 2"></button>
        <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="2" aria-label="Slide 3"></button>
      </div>

      <!-- 캐러셀 아이템 -->
      <div class="carousel-inner">
        <!-- 첫 번째 슬라이드 -->
        <div class="carousel-item active">
          <div class="content-box">
            <img src="/design/StarPot.png" alt="StarPot 이미지" class="main-image" />
            <h1 class="h1">어떤 예적금 상품을 가입할 지 고민되시나요</h1>
            <p class="p">추천을 받아보세요</p>
            <div class="inline-content">
              <img src="/design/character/star1.png" alt="StarPot 이미지" class="main-image" />
              <router-link to="/productsrecommend">
                <button class="btn btn-primary main-btn">추천 받기</button>
              </router-link>
            </div>
          </div>
        </div>

        <!-- 두 번째 슬라이드 -->
        <div class="carousel-item">
          <div class="content-box">
            <img src="/design/StarPot.png" alt="StarPot 이미지" class="main-image" />
            <h1 class="h1">예금 적금 상품에는 무엇이 있을까요</h1>
            <p class="p">전체 상품을 확인해보세요</p>
            <div class="inline-content">
              <img src="/design/character/star3.png" alt="StarPot 이미지" class="main-image" />
              <router-link to="/productslist">
                <button class="btn btn-primary main-btn">상품 확인하기</button>
              </router-link>
            </div>
          </div>
        </div>

        <!-- 세 번째 슬라이드 -->
        <div class="carousel-item">
          <div class="content-box">
            <img src="/design/StarPot.png" alt="StarPot 이미지" class="main-image" />
            <h1 class="h1">주변 은행을 찾아보세요</h1>
            <p class="p">내 주변에 있는 은행을 찾아드려요</p>
            <div class="inline-content">
              <!-- 메인 이미지 -->
              <img src="/design/character/star6.png" alt="StarPot 이미지" class="main-image" />
              <!-- 버튼 -->
              <router-link to="/bankmap">
                <button class="btn btn-primary main-btn">주변 은행찾기</button>
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- 이전/다음 버튼 -->
      <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
      </button>
      <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
      </button>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>

/* 메인 컨테이너 스타일 */
 .main-container {
  justify-content: center;
  margin:4% 0%;
}


/* 콘텐츠 박스 스타일 */
.content-box {
  text-align: center;
  background-color: #fffbe6;
  padding: 30px;
  border-radius: 10px;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 15px;
  position: relative;
}

/* 메인 이미지 */
.main-image {
  width: 20%;
  margin-bottom: 50px;
}



/* 이미지와 버튼을 같은 라인에 배치 */
.inline-content {
  display: flex; /* 수평 정렬 */
  width: 100%;
  justify-content: center; /* 가운데 정렬 */
  align-items: center; /* 수직 중앙 정렬 */
  gap: 120px; /* 이미지와 버튼 사이 간격 */
  margin-top: 20px; /* 상단 텍스트와 간격 추가 */
}

/* 메인 버튼 스타일 */
.main-btn {
  background-color: #ffc107;
  border: none;
  padding: 15px 50px;
  border-radius: 5px;
  font-size: 24px;
  cursor: pointer;
  size: 100px;
}

/* .btn-primary{
  display: inline;
} */

.main-btn:hover {
  background-color: #fcd153;
}

.carousel-control-next,
.carousel-control-prev {
  background-color: #ffffff;
  top: 50%;
  transform: translateY(-50%);
  width: 8%; /* 버튼 너비 */
  height: 100%; /* 버튼 높이 */
  filter: invert(0.3) sepia(1) saturate(5) hue-rotate(deg); /* 노란색 아이콘 */
}


/* 캐러셀 컨테이너 스타일 */
.carousel {
  position: relative;
  width: 100%;
}




</style>
