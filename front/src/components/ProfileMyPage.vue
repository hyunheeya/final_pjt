<template>
  <div class="container">
    <div v-if="userInfo">
      <div v-if="!isEditing">
        <p><strong>사용자명:</strong> {{ userInfo.username }}</p>
        <p><strong>이메일:</strong> {{ userInfo.email }}</p>
        <p><strong>닉네임:</strong> {{ userInfo.nickname }}</p>
        <button @click="startEditing" class="btn btn-primary">프로필 수정</button>
      </div>
      <form v-else @submit.prevent="updateProfile" class="mt-3">
        <div class="mb-3">
          <label for="email" class="form-label">이메일:</label>
          <input 
            id="email" 
            v-model="editedInfo.email" 
            type="email" 
            class="form-control" 
            required
          >
        </div>
        <div class="mb-3">
          <label for="nickname" class="form-label">닉네임:</label>
          <input 
            id="nickname" 
            v-model="editedInfo.nickname" 
            class="form-control" 
            required
          >
        </div>
        <button type="submit" class="btn btn-success me-2">저장</button>
        <button @click="cancelEditing" class="btn btn-secondary">취소</button>
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

const startEditing = () => {
  editedInfo.email = userInfo.value.email;
  editedInfo.nickname = userInfo.value.nickname;
  isEditing.value = true;
};

const cancelEditing = () => {
  isEditing.value = false;
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

onMounted(async () => {
  if (store.isLogin) {
    userInfo.value = await store.getUserInfo();
  }
});
</script>