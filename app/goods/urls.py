
from django.urls import path,re_path
from goods.views import IndexView
app_name = 'goods'
urlpatterns = [
    path('',IndexView.as_view(),name='index'),
]
