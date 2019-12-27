from django.db import models
from django.contrib.auth.models import AbstractUser


# 用户表
class User(AbstractUser):
    phone = models.CharField(max_length=11)
    avatar = models.ImageField(upload_to='img_avatar/', default='media/img_avatar/default.jpg')
    create_time = models.DateTimeField(auto_now_add=True)
    integral_num = models.IntegerField(default=0)  # 积分数
    is_delete = models.BooleanField(default=False)
    addr_num = models.IntegerField(default=0)   # 收货地址个数

    class Meta:
        db_table = 'User'

    def __str__(self):
        return self.username

# 积分表
class UserIntegral(models.Model):
    user = models.OneToOneField(to=User, db_constraint=False, on_delete=models.CASCADE)
    integral_num = models.IntegerField(default=0)       # 总积分
    current_integral = models.IntegerField(default=0)   # 现有积分数
    cost_num = models.IntegerField(default=0)            # 已花费积分


# 积分管理表
class Integral(models.Model):
    user = models.ForeignKey(to='User', db_constraint=False, on_delete=models.CASCADE)
    current_integral = models.IntegerField()    # 最新积分数
    increase_integral = models.IntegerField()   # 增加或减少的积分数
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Integral'

    def __str__(self):
        return '%s' %self.id


# 收货地址表
class Address(models.Model):
    user = models.ForeignKey(to=User, db_constraint=False, on_delete=models.CASCADE)
    addr = models.CharField(max_length=256)      # 收货地址
    consignee = models.CharField(max_length=64)  # 收件人
    phone = models.CharField(max_length=11)      # 收件人手机号码
    is_default = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Address'

    def __str__(self):
        return '%s' %self.id


