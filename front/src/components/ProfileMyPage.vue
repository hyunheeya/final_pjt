<template>
  <div class="container">
    <div v-if="userInfo">
      <div v-if="!isEditing && !isChangingPassword" class="profile">
        <!-- 프로필 -->
        <div class="profile-image">
          <img src="/design/character/star5.png" alt="프로필 이미지" />
        </div>
        <p><strong>아이디:</strong> {{ userInfo.username }}</p>
        <p><strong>이메일:</strong> {{ userInfo.email }}</p>
        <p><strong>닉네임:</strong> {{ userInfo.nickname }}</p>
        <button @click="startEditing" class="btn btn-success me-2">프로필 수정</button>
        <button @click="startPasswordChange" class="btn btn-warning">비밀번호 변경</button>
      </div>

      <!-- 프로필 수정 폼 -->
      <form v-if="isEditing" @submit.prevent="updateProfile" class="mt-3">
        <div class="mb-3">
          <label for="email" class="form-label">이메일:</label>
          <input id="email" v-model="editedInfo.email" type="email" class="form-control" required>
        </div>
        <div class="mb-3">
          <label for="nickname" class="form-label">닉네임:</label>
          <input id="nickname" v-model="editedInfo.nickname" class="form-control" required>
        </div>
        <button type="submit" class="btn btn-success me-2">저장</button>
        <button @click="cancelEditing" class="btn btn-secondary">취소</button>
      </form>

      <!-- 비밀번호 변경 폼 -->
      <form v-if="isChangingPassword" @submit.prevent="changePassword" class="mt-3">
        <div class="mb-3">
          <label for="currentPassword" class="form-label">현재 비밀번호:</label>
          <input id="currentPassword" v-model="passwordData.currentPassword" type="password" class="form-control" required>
        </div>
        <div class="mb-3">
          <label for="newPassword" class="form-label">새 비밀번호:</label>
          <input id="newPassword" v-model="passwordData.newPassword" type="password" class="form-control" required>
        </div>
        <div class="mb-3">
          <label for="confirmPassword" class="form-label">새 비밀번호 확인:</label>
          <input id="confirmPassword" v-model="passwordData.confirmPassword" type="password" class="form-control" required>
        </div>
        <button type="submit" class="btn btn-success me-2">변경하기</button>
        <button @click="cancelPasswordChange" class="btn btn-secondary">취소</button>
      </form>
    </div>
    <div v-else>
      <p>로딩 중...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue';
import { useCounterStore } from "@/stores/counter";
import axios from 'axios';

const store = useCounterStore();
const userInfo = ref(null);
const isEditing = ref(false);
const editedInfo = reactive({});

const isChangingPassword = ref(false);

const passwordData = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
});

const startEditing = () => {
  editedInfo.email = userInfo.value.email;
  editedInfo.nickname = userInfo.value.nickname;
  isEditing.value = true;
};

const cancelEditing = () => {
  isEditing.value = false;
};

const startPasswordChange = () => {
  isChangingPassword.value = true;
  isEditing.value = false;
};

const cancelPasswordChange = () => {
  isChangingPassword.value = false;
  passwordData.currentPassword = '';
  passwordData.newPassword = '';
  passwordData.confirmPassword = '';
};

// 개인정보 수정
const updateProfile = async () => {
  try {
    const response = await axios({
      method: 'put',
      url: `${store.API_URL}/api/accounts/profile/update/`,
      data: {
        email: editedInfo.email,
        nickname: editedInfo.nickname
      },
      headers: {
        'Authorization': `Token ${store.token}`,
        'Content-Type': 'application/json'
      }
    })
    userInfo.value = response.data
    isEditing.value = false
  } catch (error) {
    console.error('프로필 업데이트 실패:', error)
  }
};

// 비밀번호 수정
const changePassword = async () => {
  if (passwordData.newPassword !== passwordData.confirmPassword) {
    alert('새 비밀번호가 일치하지 않습니다.');
    return;
  }

  try {
    const response = await axios({
      method: 'put',
      url: `${store.API_URL}/api/accounts/change-password/`,
      data: {
        current_password: passwordData.currentPassword,
        new_password: passwordData.newPassword
      },
      headers: {
        'Authorization': `Token ${store.token}`,
        'Content-Type': 'application/json'
      }
    });

    alert('비밀번호가 성공적으로 변경되었습니다.');
    // 폼 초기화
    passwordData.currentPassword = '';
    passwordData.newPassword = '';
    passwordData.confirmPassword = '';
    // 비밀번호 변경 폼 닫기
    isChangingPassword.value = false;
  } catch (error) {
    alert(error.response?.data?.error || '비밀번호 변경에 실패했습니다.');
  }
};

onMounted(async () => {
  if (store.isLogin) {
    userInfo.value = await store.getUserInfo();
  }
});
</script>

<style scoped>
  .container{
   text-align: center;
   margin: 16%;
   padding: 10px 50px;
  }
/* 프로필 컨테이너 중앙 정렬 */
.profile-container {
  display: flex;
  flex-direction: column;
  align-items: center; /* 수평 중앙 정렬 */
  justify-content: center; /* 수직 중앙 정렬 */
  margin: 0 auto;
  text-align: center; /* 텍스트 중앙 정렬 */
  padding: 20px;
}

/* 프로필 이미지 스타일 */
.profile-image img {
  width: 150px; /* 이미지 크기 */
  height: 150px; /* 이미지 크기 */
  object-fit: cover; /* 비율 유지하며 크기 맞춤 */
  border-radius: 50%; /* 둥근 프로필 이미지 */
  margin-bottom: 20px; /* 이미지와 정보 간격 */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* 그림자 효과 */
}

/* 사용자 정보 스타일 */
.profile-info ul {
  list-style-type: none; /* 리스트 스타일 제거 */
  padding: 0;
  margin: 0;
}

.profile-info ul li {
  font-size: 18px; /* 글씨 크기 */
  margin-bottom: 10px; /* 각 항목 간 간격 */
}

/* 버튼 컨테이너 */
.profile-buttons {
  margin-top: 20px;
}

.profile-buttons .btn {
  margin: 0 10px; /* 버튼 간격 */
  padding: 10px 20px; /* 버튼 크기 조정 */
}


</style>