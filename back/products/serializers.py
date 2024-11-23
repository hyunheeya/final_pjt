from rest_framework import serializers
from .models import Deposit

class DepositSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Deposit
        fields = ['id', 'kor_co_nm', 'fin_prdt_nm', 'intr_rate', 'save_trm', 'like_count', 'is_liked']