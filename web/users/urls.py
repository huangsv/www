from django.urls import path, re_path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('login/', userlogin, name='login'),  # 登录
    path('register/', register, name='register'),  # 注册
]