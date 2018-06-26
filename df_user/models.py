from django.db import models

# Create your models here.
class UserInfo(models.Model):
    uname = models.CharField(max_length=20) #用户名
    upwd = models.CharField(max_length=40) #密码 加密
    uemail = models.CharField(max_length=30) #邮箱
    ushou = models.CharField(max_length=20,default='')#收货地址
    uaddress = models.CharField(max_length=100,default='') #详细地址
    uyoubian = models.CharField(max_length=6,default='') #邮编
    uphone = models.CharField(max_length=11,default='') #电话号码
    # default,blank是python层面的约束，不影响数据库表结构
    #也就是说不需要迁移数据库
