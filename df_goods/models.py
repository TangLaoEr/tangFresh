from django.db import models
from tinymce.models import HTMLField #富文本编辑器

# Create your models here.
#商品分类
class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = '商品类别'
    def __str__(self):
        return self.ttitle

#商品信息
class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=20,verbose_name='名称') #名称
    gpic = models.ImageField(upload_to='goods',verbose_name='图片') #图片
    gprice = models.DecimalField(max_digits=5,decimal_places=2,verbose_name='价格') #总位数 小数位
    isDelete = models.BooleanField(default=False,verbose_name='是否删除') #是否删除
    gunit = models.CharField(max_length=20,default='500g',verbose_name='单位') #单位
    gclick = models.IntegerField(verbose_name='人气') #点击率 人气
    gjianjie = models.CharField(max_length=200,verbose_name='简介') #简介
    gkucun = models.IntegerField(verbose_name='库存') #库存

    #from tinymce.models import HTMLField #富文本编辑器
    # settings里面设置 添加应用 TINYMCE_DEFAULT_CONFIG
    # 在dailyfresh里面配置url
    gcontent = HTMLField(verbose_name='商品详细介绍') #商品介绍

    #gadv = models.BooleanField(default=False)  # 推荐 广告
    gtype = models.ForeignKey(TypeInfo,on_delete=models.CASCADE) #外键 属于哪个分类

    class Meta:
        verbose_name_plural='商品信息 '


    def __str__(self):
        return self.gtitle


