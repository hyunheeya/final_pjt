<template>
  <div class="container mt-5">
    <h1 class="text-center mb-4">회원가입</h1>
    <form @submit.prevent="signUp" class="w-50 mx-auto p-4 border rounded shadow-sm bg-light">
      <div class="mb-3">
        <label for="username" class="form-label">아이디</label>
        <input
          type="text"
          id="username"
          v-model.trim="username"
          class="form-control"
          placeholder="아이디를 입력하세요"
        >
      </div>
      <div class="mb-3">
        <label for="email" class="form-label">이메일</label>
        <input
          type="email"
          id="email"
          v-model.trim="email"
          class="form-control"
          placeholder="이메일 주소를 입력하세요"
        >
      </div>
      <div class="mb-3">
        <label for="nickname" class="form-label">닉네임</label>
        <input
          type="text"
          id="nickname"
          v-model.trim="nickname"
          class="form-control"
          placeholder="닉네임을 입력하세요"
        >
      </div>
      <div class="mb-3">
        <label for="password1" class="form-label">비밀번호</label>
        <input
          type="password"
          id="password1"
          v-model.trim="password1"
          class="form-control"
          placeholder="비밀번호를 입력하세요"
        >
      </div>
      <div class="mb-3">
        <label for="password2" class="form-label">비밀번호 확인</label>
        <input
          type="password"
          id="password2"
          v-model.trim="password2"
          class="form-control"
          placeholder="비밀번호를 다시 입력하세요"
        >
      </div>
      <div class="text-center">
        <input
          type="submit"
          value="회원가입"
          class="btn btn-success w-100"
        >
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'

const username = ref(null)
const email = ref(null)
const nickname = ref(null)
const password1 = ref(null)
const password2 = ref(null)

const store = useCounterStore()

const signUp = function () {
  const payload = {
    username: username.value,
    email: email.value,
    nickname: nickname.value,
    password1: password1.value,
    password2: password2.value
  }
  store.signUp(payload)
}
</script>

<style scoped>
</style>
