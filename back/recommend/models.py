from django.db import models

# Create your models here.

class Deposit(models.Model):
    name = models.CharField(max_length=100)
    interest_rate = models.FloatField()
    saving_period = models.CharField(max_length=50)
    joining_method = models.CharField(max_length=50)
    interest_type = models.CharField(max_length=10)

    class Meta:
        db_table = 'deposit_table'  # 첫 번째 DB 테이블 이름
        managed = False  # 이미 생성된 테이블 사용 시 False


class Savings(models.Model):
    name = models.CharField(max_length=100)
    interest_rate = models.FloatField()
    saving_period = models.CharField(max_length=50)
    joining_method = models.CharField(max_length=50)
    interest_type = models.CharField(max_length=10)

    class Meta:
        db_table = 'savings_table'  # 두 번째 DB 테이블 이름
        managed = False