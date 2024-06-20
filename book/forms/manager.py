"""
code speace
@Time    : 2024/4/13 10:59
@Author  : 泪懿:dgl
@File    : manager.py
"""
from django import forms
from book import models
from .bookstrap import BootStrapForm
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from book.models import User
from book.uitls import encrypt
class UserLoginModelForm(BootStrapForm,forms.ModelForm):
    """
    后台登录管理员表单
    """

    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.request=request

    password = forms.CharField(label='密码', widget=forms.PasswordInput(

    ))
    code = forms.CharField(label='验证码', widget=forms.TextInput(attrs={

    }))
    class Meta:
        model=User
        fields=['username','password','code']


    def clean_username(self):
        """
        处理校验数据
        :return:
        """
        username=self.cleaned_data['username']
        user_obj = User.objects.filter(username=username).exists()
        if not user_obj:
            #主动添加错误
            self.add_error('username','用户不存在')

        return username

    def clean_password(self):

        password=self.cleaned_data['password']

        username = self.cleaned_data['username']

        user_obj =  models.User.objects.filter(username=username).first()
        if user_obj:
            if user_obj.password!=password:
                raise ValidationError('密码错误，请重新输入')

        return password

    def clean_code(self):
        code = self.cleaned_data['code']
        #往session取验证码
        session_code = self.request.session.get('captch_code')
        if not session_code:
            raise ValidationError("验证码过期，请重新点击")
        if code.upper().strip() != session_code.upper():
            raise ValidationError("验证码输入错误")
        return code

class BookModelForm(BootStrapForm,forms.ModelForm):

    class Meta:
        model=models.BookInfo
        exclude=['create_datetime','booklogo','booktype']



class UserModelForm(BootStrapForm,forms.ModelForm):
    """
    用户表单
    """
    class Meta:
        model=models.Userinfo
        exclude=[
            'avator'
        ]

    def clean_mobile_phone(self):

        phone = self.cleaned_data['mobile_phone']
        user_obj=models.Userinfo.objects.filter(mobile_phone=phone)
        if user_obj.exists():
            if user_obj.first()!=self.instance:
                raise ValidationError('手机号已被注册')
        return phone

    def clean_email(self):
        email = self.cleaned_data['email']

        user_obj = models.Userinfo.objects.filter(email=email)
        if user_obj.exists():
            if user_obj.first() != self.instance:
                raise ValidationError('邮箱已被注册')
        return email

    def clean_password(self):
        password = self.cleaned_data['password']

        return encrypt.md5(password)

