from cart.views import CartAddView,CartInfoView,CarUpdateView,CartDeleteView
from django.urls import path,re_path
app_name = 'cart'
urlpatterns = [
    path('',CartInfoView.as_view(),name='show'),  #购物车页面显示
    path('add',CartAddView.as_view(),name='add'),  #购物车记录添加
    path('update',CarUpdateView.as_view(),name='update'),  #购物车记录更新
    path('delete',CartDeleteView.as_view(),name='delete'),  #购物车商品删除
]
