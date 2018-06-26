from django.shortcuts import render,redirect
from df_user import user_decorator
from df_user.models import *
from df_cart.models import *
from django.db import transaction #事务
from df_order.models import *
from datetime import datetime
# Create your views here.
@user_decorator.login
def order(request):
    #查询用户对象
    user = UserInfo.objects.get(id=request.session['user_id'])
    #根据提交查询购物车信息
    get = request.GET
    cart_ids = get.getlist('cart_id')
    cart_ids1 = [int(item) for item in cart_ids]
    carts = CartInfo.objects.filter(id__in=cart_ids1)

    context = {
        'title':'提交订单',
        'page_name':1,
        'carts':carts,
        'user':user,
        'cart_ids':','.join(cart_ids)
    }
    return render(request,'df_order/order.html',context)

'''
事务：一旦操作失败则全部回退
1、创建订单对象
2、判断商品的库存
3、创建详单对象
4、修改商品库存
5、删除购物车
'''
@transaction.atomic() #事务：一旦操作失败则全部回退
@user_decorator.login
def order_handle(request):
    tran_id = transaction.savepoint()

    #接收购物车编号
    cart_ids = request.POST.get('cart_ids')
    try:
        #创建订单对象
        order = OrderInfo()
        now = datetime.now()
        uid = request.session['user_id']
        order.oid = '%s%d'%(now.strftime('%Y%m%d%H%M%S'),uid)
        order.user_id = uid
        order.odate = now
        order.oaddress = request.POST.get('address')
        order.ototal = 0 #？？？？？？？？？？？？？？？？疑问？？？？？？？？？？？？？？？？？？？？？？
        order.save()

        #创建详单对象
        cart_ids1 = [int(item) for item in cart_ids.split(',')]
        total = 0

        for id1 in cart_ids1:
            detail1 = OrderDetailInfo()
            detail1.order = order

            #查询购物车信息
            cart = CartInfo.objects.get(id=id1)
            # 判断商品库存
            goods = cart.goods
            if goods.gkucun >= cart.count: #如果库存大于购买数量
                #减少商品库存
                goods.gkucun = cart.goods.gkucun-cart.count
                goods.save() #保存商品 记录库存
                #完善详单信息
                detail1.goods_id = goods.id

                price = goods.gprice
                detail1.price = price

                count = cart.count
                detail1.count = count

                detail1.save()
                total = total+price*count
                # 删除购物车数据
                cart.delete()

            else:
                #库存小于购买数量，回退到点
                transaction.savepoint_rollback(tran_id)
                return redirect('/cart/')

        #保存总价
        order.ototal = total+10 #加运费
        order.save()
        transaction.savepoint_commit(tran_id) #保存提交 所有的修改都生效

    except Exception as e:
        print('=================%s')%e
        transaction.savepoint_rollback(tran_id)

    return redirect('/user/order/')

@user_decorator.login
def pay(request,oid):
    order = OrderInfo.objects.get(oid=oid)
    order.oIsPay = True
    order.save()
    context={'order':order}
    return  render(request,'df_order/pay.html',context)




