import { ref } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useRouter } from "vue-router";

export const useCounterStore = defineStore("counter", () => {
  const API_URL = "http://127.0.0.1:8000";
  const token = ref(localStorage.getItem("token") || null);
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
      console.error("로그인 실패:", err.response?.data || err);
    }
  };

  // 로그아웃
  const logOut = () => {
    token.value = null;
    localStorage.removeItem("token");
    router.push({ name: "login" });
  };

  return { API_URL, token, signUp, logIn, logOut };
});
