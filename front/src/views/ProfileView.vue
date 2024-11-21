<template>
  <div class="profile">
    <h1>프로필</h1>
    <div v-if="userInfo">
      <div v-if="!isEditing">
        <p><strong>사용자명:</strong> {{ userInfo.username }}</p>
        <p><strong>이메일:</strong> {{ userInfo.email }}</p>
        <p><strong>닉네임:</strong> {{ userInfo.nickname }}</p>
        <!-- <button @click="startEditing">프로필 수정</button> -->
      </div>
      <form v-else @submit.prevent="updateProfile">
        <div>
          <label for="nickname">닉네임:</label>
          <input id="nickname" v-model="editedInfo.nickname" required>
        </div>
        <!-- 다른 수정 가능한 필드들 추가 -->
        <button type="submit">저장</button>
        <button @click="cancelEditing">취소</button>
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

const store = useCounterStore();
const userInfo = ref(null);
const isEditing = ref(false);
const editedInfo = reactive({});

onMounted(async () => {
  if (store.isLogin) {
    userInfo.value = await store.getUserInfo();
  }
});

const startEditing = () => {
  editedInfo.nickname = userInfo.value.nickname;
  isEditing.value = true;
};

const cancelEditing = () => {
  isEditing.value = false;
};

const updateProfile = async () => {
  try {
    // API를 통해 프로필 정보 업데이트
    // 예: await store.updateUserInfo(editedInfo);
    userInfo.value = { ...userInfo.value, ...editedInfo };
    isEditing.value = false;
  } catch (error) {
    console.error('프로필 업데이트 실패:', error);
  }
};
</script>