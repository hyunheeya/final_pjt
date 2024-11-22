from django.db import models
from accounts.models import User

# 예금
class Deposit(models.Model):
    kor_co_nm = models.CharField(max_length=255, null=True)  # 금융회사명
    fin_prdt_nm = models.CharField(max_length=255, null=True)  # 금융상품명
    join_way = models.CharField(max_length=255, null=True, blank=True)  # 가입 방법
    join_member = models.CharField(max_length=255, null=True, blank=True)  # 가입 대상
    join_price = models.IntegerField(null=True, blank=True)  # 가입 금액
    intr_rate_type = models.CharField(max_length=255, null=True, blank=True)  # 이자율 종류
    intr_rate_type_nm = models.CharField(max_length=255, null=True, blank=True)  # 이자율 종류명
    save_trm = models.IntegerField(null=True, blank=True)  # 저축 기간
    intr_rate = models.FloatField(null=True, blank=True)  # 기본 이자율
    intr_rate2 = models.FloatField(null=True, blank=True)  # 우대 이자율
    age_range = models.CharField(max_length=50, null=True, blank=True)  # 나이 제한

    class Meta:
        db_table = 'deposit_recommend'  # 테이블 이름

# 적금
class Savings(models.Model):
    kor_co_nm = models.CharField(max_length=255, null=True)  # 금융회사명
    fin_prdt_nm = models.CharField(max_length=255, null=True)  # 금융상품명
    join_way = models.CharField(max_length=255, null=True, blank=True)  # 가입 방법
    join_member = models.CharField(max_length=255, null=True, blank=True)  # 가입 대상
    etc_note = models.TextField(null=True, blank=True)  # 기타 조건
    intr_rate_type = models.CharField(max_length=255, null=True, blank=True)  # 이자율 종류
    intr_rate_type_nm = models.CharField(max_length=255, null=True, blank=True)  # 이자율 종류명
    rsrv_type = models.CharField(max_length=255, null=True, blank=True)  # 적립 유형
    rsrv_type_nm = models.CharField(max_length=255, null=True, blank=True)  # 적립 유형명
    save_trm = models.IntegerField(null=True, blank=True)  # 저축 기간
    intr_rate = models.FloatField(null=True, blank=True)  # 기본 이자율
    intr_rate2 = models.FloatField(null=True, blank=True)  # 우대 이자율
    age_range = models.CharField(max_length=50, null=True, blank=True)  # 나이 제한
    join_price = models.CharField(max_length=50, null=True, blank=True)  # 가입 금액

    class Meta:
        db_table = 'savings_recommend'  # 테이블 이름


# 예금 댓글
class DepositComment(models.Model):
    deposit = models.ForeignKey(Deposit, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# 예금 좋아요
class DepositLike(models.Model):
    deposit = models.ForeignKey(Deposit, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

# 적금 댓글
class SavingsComment(models.Model):
    savings = models.ForeignKey(Savings, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# 적금 좋아요
class SavingsLike(models.Model):
    savings = models.ForeignKey(Savings, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
