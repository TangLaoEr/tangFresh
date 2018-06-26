from django.shortcuts import render,redirect,HttpResponseRedirect
from .models import *
from hashlib import sha1 #对密码加密
from . import user_decorator
from df_goods.models import *
from df_order.models import *
from django.core.paginator import Paginator,Page


# Create your views here.
def register(request):
    return render(request,'df_user/register.html')

def register_handle(request):
    #接受注册用户输入
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')
    #判断两次密码是否一样
    if upwd != upwd2:
        print('nihao')
        return redirect('/user/register/')

    #密码加密
    s1 = sha1()
    s1.update(upwd.encode('utf-8'))
    upwd3 = s1.hexdigest()

    #创建对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()
    #注册成功 转到登录页面
    return redirect('/user/login/')

def login(request):
    uname = request.COOKIES.get('uname','')
    context = {'title':'用户登录','error_name':0,'error_pwd':0,'uname':uname}
    return render(request, 'df_user/login.html',context)

def login_handle(request):
    #接收请求信息
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu',0)
    users = UserInfo.objects.filter(uname=uname) #根据用户名查询对象
    if len(users) == 1:
        s1 = sha1()
        s1.update(upwd.encode('utf-8'))
        print(s1.hexdigest())
        if s1.hexdigest() == users[0].upwd:
            #密码正确
            url = request.COOKIES.get('url','/')
            red = HttpResponseRedirect(url)

            red.set_cookie('url','',max_age=-1)
            if jizhu != 0:
                red.set_cookie('uname',uname)
            else:
                red.set_cookie('uname','',max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname

            return red
        else:
            context = {'title':'用户登录','error_name':0,'error_pwd':1,'uname':uname,'upwd':upwd}
            return render(request, 'df_user/login.html', context)
    else:
        context = {'title':'用户登录','error_name':1,'error_pwd':0,'uname':uname,'upwd':upwd}
        return render(request,'df_user/login.html',context)

def logout(request):
    request.session.flush()
    return redirect('/')

#利用装饰器查看是否有登录
#个人信息
@user_decorator.login
def info(request):
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail
    #最近浏览
    goods_list = []
    goods_ids = request.COOKIES.get('goods_ids','') #哪里设置了浏览cookies 在df_goods.views
    if goods_ids != '':
        goods_ids1 = goods_ids.split(',')
        for goods_id in goods_ids1:
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))

    context = {
        'title':'用户中心',
        'user_email':user_email,
        'user_name':request.session['user_name'],
        'page_name':1,
        'goods_list':goods_list
    }
    return render(request,'df_user/user_center_info.html',context)

#订单
@user_decorator.login
def order(request,pindex):
    order_list = OrderInfo.objects.filter(user_id=request.session['user_id']).order_by('-oid')
    paginator = Paginator(order_list,2)
    if pindex == '':
        pindex = '1'
    page = paginator.page(int(pindex))
    context = {
        'title':'用户中心',
        'page_name':1,
        'paginator':paginator,
        'page':page
    }
    return render(request,'df_user/user_center_order.html',context)


#在user_center_info 里面的收货地址
@user_decorator.login
def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uyoubian = post.get('uyoubian')
        user.uphone = post.get('uphone')
        user.save()

    context = {
        'title':'用户中心',
        'user':user,
        'page_name':1
    }
    return render(request,'df_user/user_center_site.html',context)



