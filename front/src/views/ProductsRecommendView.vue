<template>
  <div class="container text-center mt-5">
    <h1 class="display-4 mb-4 fw-bold">예적금 상품 추천</h1>
    <h5>나에게 맞는 금융 상품을 추천받아보세요!</h5>
    <div>
      <img :src="randomImage" alt="Random Character" class="img">
    </div>
    <RouterLink :to="{name: 'productsrecommendquiz'}">
      <button class="btn btn-warning btn-lg">시작하기</button>
    </RouterLink>
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
    }
  },
  mounted() {
    this.setRandomImage()
  },
  methods: {
    setRandomImage() {
      const randomIndex = Math.floor(Math.random() * this.images.length)
      this.randomImage = this.images[randomIndex]
    }
  }
}
</script>

<style scoped>
  .img{
  width: 32%;
  padding: 40px;
  }

</style>