from user.views import RegisterView,ActiveView,LoginView
from django.urls import path,re_path

app_name='user'
urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    re_path('active/(?P<token>.*)$',ActiveView.as_view(),name='active')

]
