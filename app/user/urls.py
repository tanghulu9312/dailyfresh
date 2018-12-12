from user.views import RegisterView,ActiveView,LoginView,UserInfoView,UserOrderView,UserAddressView,LogoutView
from django.urls import path,re_path
from django.contrib.auth.decorators import login_required

app_name='user'
urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),   #用户注册
    path('login/',LoginView.as_view(),name='login'),    #用户登录
    path('logout/',LogoutView.as_view(),name='logout'),    #注销登录
    re_path('active/(?P<token>.*)$',ActiveView.as_view(),name='active'),    #用户激活
    path('',UserInfoView.as_view(),name='user'),    #用户信息
    path('order/',UserOrderView.as_view(),name='order'),    #用户订单
    path('address/',UserAddressView.as_view(),name='address'),   #用户地址

]
