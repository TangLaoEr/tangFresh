from django.db import models

# Create your models here.

#关联别的应用的models 需要应用的名字（点） 类
class CartInfo(models.Model):
    user = models.ForeignKey('df_user.UserInfo',on_delete=models.CASCADE)
    goods = models.ForeignKey('df_goods.GoodsInfo',on_delete=models.CASCADE)
    count = models.IntegerField() #数量