import { ref,computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useRouter } from "vue-router";

export const useCounterStore = defineStore("counter", () => {
  const API_URL = "http://127.0.0.1:8000";
  const token = ref(localStorage.getItem("token") || null);

  // 로그인 여부 확인
  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })
  const router = useRouter();

  // 회원가입
  const signUp = async (payload) => {
    try {
      const { username, email, nickname, password1, password2 } = payload;

      await axios.post(`${API_URL}/accounts/signup/`, {
        username,
        email,
        nickname,
        password1,
        password2,
      });

      // 회원가입 후 자동 로그인
      await logIn({ username, password: password1 });
    } catch (err) {
      alert('회원정보를 다시 확인해주세요.')
      console.error("회원가입 실패:", err.response?.data || err);
    }
  };

  // 로그인
  const logIn = async (payload) => {
    try {
      const { username, password } = payload;

      const response = await axios.post(`${API_URL}/accounts/login/`, {
        username,
        password,
      });

      token.value = response.data.key;
      localStorage.setItem("token", token.value);

      router.push({ name: "home" });
    } catch (err) {
      alert('아이디 및 비밀번호를 확인해주세요!')
      console.error("로그인 실패:", err.response?.data || err);
    }
  };

  // 로그아웃
  const logOut = async () => {
  try {
    // 서버에 로그아웃 요청 (필요한 경우)
    // await axios.post(`${API_URL}/accounts/logout/`);

    // 로컬 상태 및 스토리지 정리
    token.value = null;
    localStorage.removeItem("token");

    // 홈 페이지로 리다이렉트
    router.push({ name: "home" });
  } catch (err) {
    console.error("로그아웃 실패:", err);
  }
  };

  return { API_URL, token, isLogin, signUp, logIn, logOut };
});
