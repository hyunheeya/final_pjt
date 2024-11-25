<template>
  <div class="container mt-5">
    <h1 class="text-center mb-4">로그인</h1>
    <form @submit.prevent="logIn" class="w-50 mx-auto p-4 border rounded shadow-sm bg-light">
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
        <label for="password" class="form-label">비밀번호</label>
        <input
          type="password"
          id="password"
          v-model.trim="password"
          class="form-control"
          placeholder="비밀번호를 입력하세요"
        >
      </div>
      <div class="text-center">
        <input
          type="submit"
          value="로그인"
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
const password = ref(null)

const store = useCounterStore()

const logIn = function () {
  const payload = {
    username: username.value,
    password: password.value
  }
  store.logIn(payload)
}
</script>

<style scoped>
</style>
