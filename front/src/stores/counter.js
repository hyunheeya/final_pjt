import { ref,computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useRouter } from "vue-router";

export const useCounterStore = defineStore("counter", () => {
  const API_URL = "http://127.0.0.1:8000"
  const token = ref(localStorage.getItem("token") || null)
  const userInfo = ref(null)
  const articles = ref([])
  const isLoading = ref(false)

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

  // 유저 정보 가져오기
  const getUserInfo = async () => {
    if (isLogin.value && !userInfo.value) {
      try {
        const response = await axios.get(`${API_URL}/api/accounts/user-info/`, {
          headers: { 
            'Authorization': `Token ${token.value}`,
            'Content-Type': 'application/json',
          },
          withCredentials: true
        });
        userInfo.value = response.data;
      } catch (error) {
        console.error('사용자 정보 가져오기 실패:', error);
        userInfo.value = null;
        // 토큰이 유효하지 않은 경우 로그아웃 처리
        if (error.response?.status === 401) {
          token.value = null;
          localStorage.removeItem("token");
        }
      }
    }
    return userInfo.value;
  };

  // 로그아웃
  const logOut = async () => {
    try {
      // 서버에 로그아웃 요청
      await axios.post(`${API_URL}/accounts/logout/`, {}, {
        headers: {
          'Authorization': `Token ${token.value}`
        }
      });
      
      token.value = null;
      localStorage.removeItem("token");
      userInfo.value = null;  // 사용자 정보도 초기화
      
      router.push({ name: "home" });
    } catch (err) {
      console.error("로그아웃 실패:", err);
      // 에러가 발생해도 로컬 상태는 초기화
      token.value = null;
      localStorage.removeItem("token");
      userInfo.value = null;
    }
  };

  // 게시글 목록 가져오기
  const fetchArticles = async () => {
    isLoading.value = true;
    try {
      const response = await axios.get(`${API_URL}/api/board/articles/`, {
        headers: { 'Authorization': `Token ${token.value}` }
      });
      articles.value = response.data;
    } catch (err) {
      console.error("게시글 목록 가져오기 실패:", err);
    } finally {
      isLoading.value = false;
    }}
  // 관리자 여부 확인
  const checkAdminStatus = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/board/check-admin/`, {
        headers: { 'Authorization': `Token ${token.value}` }
      });
      return response.data.is_admin;
    } catch (err) {
      console.error("관리자 상태 확인 실패:", err);
      return false;
    }
  }

  return { API_URL, token, userInfo, isLogin, articles, isLoading, signUp, logIn, getUserInfo, logOut, fetchArticles, checkAdminStatus };
});
export default useCounterStore