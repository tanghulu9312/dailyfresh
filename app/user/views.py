from django.shortcuts import render,redirect,HttpResponse
from django.urls import reverse
from user.models import User
from django.views import View
from django import forms
from django.forms import widgets,fields
import re
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.conf import settings
from celery_tasks.tasks import send_register_active_email
from django.contrib.auth import authenticate,login

# Create your views here.

class RegisterVerify(forms.Form):
    user = fields.CharField(
        error_messages={'required':'用户名不能为空'},
        label='用户名',
    )
    pwd = fields.CharField(
        error_messages={'required':'密码不能为空'},
        label = '密码',
    )

    email = fields.EmailField(
        error_messages={'required':'邮箱不能为空','invalid':'邮箱格式错误'},
        label='邮箱',
    )


class RegisterView(View):
    def get(self,request):
        #返回注册页面
        # obj = RegisterVerify()
        return render(request,'register.html')

    def post(self,request):
        #接收数据
        username = request.POST.get('user_name');
        passwrod = request.POST.get('pwd');
        cpasswrod = request.POST.get('cpwd');
        email = request.POST.get('email');
        allow = request.POST.get('allow');

        #进行数据校验
        if not all([username,passwrod,email]):
            #数据不完整
            return render(request,'register.html',{'errmsg':"数据不完整"})
        # obj = RegisterVerify(request.POST)
        # res = obj.is_valid()
        # if res:
        #     return render(request,'index.html',{'username':obj.cleaned_data['user']})
        # else:
        #     return render(request,'register.html',{'obj':obj})
        #校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
            return render(request,'register.html',{'errmsg':'邮箱格式不正确'})
        if allow != 'on':
            return render(request,'register.html',{'errmsg':'请同意使用协议'})
        #校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            #用户名不存在
            user = None
        if user:
            #用户名已经存在
            return render(request,'register.html',{'errmsg':'用户名已经存在'})
        #进行业务处理：进行用户注册
        user = User.objects.create_user(username,email,passwrod)
        user.is_active=0
        user.save()
        #发送激活邮件，包含激活链接：http://127.0.0.1:8000/user/active/...
        #激活链接中需包含用户的身份信息，并且要把身份信息进行加密

        #加密用户的身份信息，生成激活token
        serializer = Serializer(settings.SECRET_KEY,3600)
        info = {'confirm':user.id}
        token = serializer.dumps(info)
        token = token.decode()  #bytes数据转成utf-8字符串

        #发邮件
        send_register_active_email(email,username,token)
        
        #返回应答，跳转到首页
        return redirect(reverse('goods:index'))
class ActiveView(View):
    '''用户激活'''
    def get(self,request,token):
        #进行用户激活
        #进行解密，获取要激活的用户信息
        serializer = Serializer(settings.SECRET_KEY,3600)
        try:
            info = serializer.loads(token)
            #获取待激活用户的ID
            user_id = info['confirm']
            #根据ID获取用户信息
            user=User.objects.get(id=user_id)
            user.is_active=1
            user.save()
            #跳转到登录界面
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            #激活链已过期
            return HttpResponse('激活链接已过期')

class LoginView(View):
    #登录
    def get(self,request):
        '''显示登录页面'''
        #判断是否记住了用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''

        return render(request,'login.html',{'username':username,'checked':checked})
    def post(self,request):
        #获取客户端提交过来的post数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        remenber = request.POST.get('remenber')
        #校验数据
        if not all([username,password]):
            return render(request,'login.html',{'errmsg':'数据不完整'})
        #业务处理：登录校验
        user = authenticate(username=username,password=password)
        if user is not None:
            #用户名密码正确
            if user.is_active:
                #用户已激活
                #记录用户登录状态
                login(request,user)
                #跳转到首页
                response = redirect(reverse('goods:index'))

                #判断用户是否需要记住用户名
                if remenber == 'on':
                    #记住用户名
                    response.set_cookie('username',username,max_age=7*24*60)
                else:
                    response.delete_cookie('username')
                #返回response
                return response
            else:
                #用户未激活
                return render(request,'login.html',{'errmsg':'账户未激活'})
        else:
            #用户名或密码错误
            return  render(request,'login.html',{'errmsg':'用户名或密码错误'})




