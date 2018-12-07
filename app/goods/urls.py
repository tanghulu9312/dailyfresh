
from django.urls import path
from goods.views import IndexView
app_name='[goods]',
urlpatterns = [
    path('index/',IndexView.as_view(),name='index'),
]
