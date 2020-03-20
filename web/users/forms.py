from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


# 注册表单类
class RegisterForm(forms.Form):
    # 用户名字段
    username = forms.CharField(min_length=4, max_length=16, label='用户名', required=True, error_messages={
        'required': '请填写你的用户名，用于登录',
        'min_length': '至少输入 4 个字符',
        'max_length': '最多只能输入 16 个字符',
    }, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'username',
        'placeholder': '请输入用户名',
    }))  # required默认为Ture，必填
    # 邮箱
    email = forms.EmailField(max_length=30, label='邮箱', required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'useremail',
        'placeholder': '请输入电子邮箱,注册后不可更改！',
    }))
    # 密码字段
    password = forms.CharField(min_length=6, max_length=16, label='密码', error_messages={
        'min_length': '至少输入 6 个字符',
        'max_length': '最多只能输入 16 个字符',
    }, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'userpwd',
        'placeholder': '请输入密码',
    }))
    # 确认密码字段
    confirm_password = forms.CharField(max_length=16, label='re密码', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'userrepwd',
        'placeholder': '再次确认密码',
    }))
    # 验证码
    # verify_code = forms.CharField(max_length=4, label='验证码', widget=forms.TextInput(attrs={
    #     'class': 'form-control',
    #     'id': 'verifycode',
    #     'placeholder': '请输入验证码'
    # }))

    # 验证
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # if len(username) < 4:
        #     raise forms.ValidationError(u'用户名不少于 4 个字符!')
        # if username == '' and email == '' and password == '' and confirm_password == '':
        #     return None
        # else:
        username_list = ['admin']

        reusername = User.objects.filter(username=username)
        for u in reusername:
            username_list.append(u.username)
        reemail = User.objects.filter(email=email)
        email_list = []
        for e in reemail:
            email_list.append(e.email)

        if username in username_list:
            raise forms.ValidationError(u'已存在的用户名')
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError(u'再次密码输入不一致!')
        if email in email_list:
            raise forms.ValidationError(u'已存在的邮箱')
        # elif username == '' and email == '' and password == '' and confirm_password == '':
        #     return None

    # 保存到数据库中
    def save(self):
        user = User()
        user.username = self.cleaned_data['username'].lower()
        user.email = self.cleaned_data['email'].lower()
        user.set_password(self.cleaned_data['password'])
        user.save()


# 登录表单类
class LoginForm(forms.Form):
    # 用户名字段
    username = forms.CharField(max_length=16, label='用户名', required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '请输入用户名',
    }))  # required默认为Ture，必填
    # 密码字段
    password = forms.CharField(max_length=16, label='密  码', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': '请输入密码',
    }))

    # 较验函数
    def clean(self):
        '''验证方法，在views.py中的is_valid'''
        username = self.cleaned_data['username'].lower()
        password = self.cleaned_data['password']

        user = auth.authenticate(username=username, password=password)  # 判断 用户密码是否输入正
        if user is None:
            raise forms.ValidationError('用户名或密码不正确！')  # 返回的错误提示信息
        else:
            self.cleaned_data['user'] = user  # 将 user 的信息存储到cleaned_data字典中
        return self.cleaned_data  # 必须返回cleaned_data