from django.db import models
from accounts.models import User
from recommend.models import Deposit,Savings

# 예금
class DepositComment(models.Model):
    deposit = models.ForeignKey(Deposit, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class DepositLike(models.Model):
    deposit = models.ForeignKey(Deposit, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

# 적금
class SavingsComment(models.Model):
    deposit = models.ForeignKey(Savings, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class SavingsLike(models.Model):
    deposit = models.ForeignKey(Savings, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
