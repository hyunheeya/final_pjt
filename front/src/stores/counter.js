// import { ref, computed } from 'vue'
// import { defineStore } from 'pinia'
// import axios from 'axios'
// import { useRouter } from 'vue-router'

// export const useCounterStore = defineStore('counter', () => {
//   const API_URL = 'http://127.0.0.1:8000'
//   const token = ref(null)
//   const router = useRouter()

//   // 회원가입
//   const signUp = function (payload) {
//     const { username, password1, password2 } = payload

//     axios({
//       method: 'post',
//       url: `${API_URL}/accounts/signup/`,
//       data: {
//         username, password1, password2
//       }
//     })
//       .then((res) => {
//         const password = password1
//         logIn({ username, password })
//       })
//       .catch((err) => {
//         console.log(err)
//       })
//   }

//   // 로그인
//   const logIn = function (payload) {
//     const { username, password } = payload

//     axios({
//       method: 'post',
//       url: `${API_URL}/accounts/login/`,
//       data: {
//         username, password
//       }
//     })
//       .then((res) => {
//         token.value = res.data.key
//         router.push({ name: 'home' })
//       })
//       .catch((err) => {
//         console.log(token.value)
//         console.log(err)
//       })
//   }

//   return { API_URL, token, signUp, logIn }
// }, { persist: true })

import { ref } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useRouter } from "vue-router";

export const useCounterStore = defineStore("counter", () => {
  const API_URL = "http://127.0.0.1:8000";
  const token = ref(localStorage.getItem("token") || null); // 로컬 스토리지에서 토큰 불러오기
  const router = useRouter();

  // 회원가입
  const signUp = async (payload) => {
    try {
      const { username, password1, password2 } = payload;

      await axios.post(`${API_URL}/accounts/signup/`, {
        username,
        password1,
        password2,
      })

      // 회원가입 후 자동 로그인
      await logIn({ username, password: password1 })
    } catch (err) {
      console.error("회원가입 실패:", err.response?.data || err)
    }
  }

  // 로그인
  const logIn = async (payload) => {
    try {
      const { username, password } = payload;

      const response = await axios.post(`${API_URL}/accounts/login/`, {
        username,
        password,
      })

      token.value = response.data.key; // 서버에서 반환된 토큰 저장
      localStorage.setItem("token", token.value); // 로컬 스토리지에 저장

      // 로그인 후 홈으로 이동
      router.push({ name: "home" });
    } catch (err) {
      console.error("로그인 실패:", err.response?.data || err)
    }
  };

  // 로그아웃
  const logOut = () => {
    token.value = null;
    localStorage.removeItem("token"); // 로컬 스토리지에서 토큰 제거
    router.push({ name: "login" }); // 로그인 페이지로 이동
  };

  return { API_URL, token, signUp, logIn, logOut }
})
