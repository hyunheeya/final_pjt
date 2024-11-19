
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User

class CustomRegisterSerializer(RegisterSerializer):
 # 필요한 필드들 추가
 email = serializers.EmailField(required=True) # 필수
 nickname = serializers.CharField(required=False,allow_blank=True,max_length=255)
 # 해당 필드도 저장 시 함께 사용하도록 설정
 def get_cleaned_data(self):
    return {
    'username': self.validated_data.get('username', ''),
    'email': self.validated_data.get('email', ''),
    'password1': self.validated_data.get('password1', ''),
    # nickname 필드 추가
    'nickname': self.validated_data.get('nickname', ''),
    }