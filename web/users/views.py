from django.shortcuts import render, redirect
from django.contrib import auth
from django.urls import reverse
from django.views import View
# Create your views here.

# 登录
from .forms import LoginForm, RegisterForm


def userlogin(request):
    '''登录'''
    # 判断是否登录
    if request.user.is_authenticated:
        return redirect('user:personal')
    if request.method == 'POST':
        login_form = LoginForm(request.POST)  # 将参数传入表单
        if login_form.is_valid():  # Django表单自动验证合法性
            # 返回的是一个字典，取出 user
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            request.session['user'] = login_form.cleaned_data['username']
            return redirect(request.GET.get('form', reverse('home:index')))
            # return render(request, 'user/successful.html', {'username': username,
                                                            # 'msg': '登录成功！'})
    else:
        login_form = LoginForm()

    return render(request, 'userlogin.html', {'login_form': login_form})


# 登出
def userlogout(request):
    auth.logout(request)
    return redirect("user:login")


# 注册
def register(request):
    # 判断是否登录
    if request.user.is_authenticated:
        return redirect('user:personal')
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)  # 将参数传入表单
        if register_form.is_valid():  # Django表单自动验证合法性
            '''is_valid()在forms.py中定义的def clean'''
            # username = register_form.cleaned_data['username']
            # 保存
            register_form.save()
            # 登录
            user = auth.authenticate(username=register_form.cleaned_data['username'], password=register_form.cleaned_data['password'])
            auth.login(request, user)
            request.session['user'] = register_form.cleaned_data['username']

            return redirect(request.GET.get('form', reverse('user:login')))
    else:
        register_form = RegisterForm()

    return render(request, 'user/register.html', {'register_form': register_form})