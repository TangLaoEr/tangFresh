from django.db import models

# Create your models here.
class OrderInfo(models.Model):
    oid = models.CharField(max_length=20,primary_key=True) #订单号 order.oid = '%s%d'%(now.strftime('%Y%m%d%H%M%S'),uid)
    user = models.ForeignKey('df_user.UserInfo',on_delete=models.CASCADE) #用户
    odate = models.DateTimeField(auto_now_add=True) #下单时间
    oIsPay = models.BooleanField(default=False) #是否付款
    ototal = models.DecimalField(max_digits=6,decimal_places=2)#总价
    oaddress = models.CharField(max_length=150) #地址

class OrderDetailInfo(models.Model):
    goods = models.ForeignKey('df_goods.GoodsInfo',on_delete=models.CASCADE)
    order = models.ForeignKey(OrderInfo,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    count = models.IntegerField() #数量