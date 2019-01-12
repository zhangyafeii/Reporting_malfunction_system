# -*- coding: utf-8 -*-

"""
@Datetime: 2018/9/26
@Author: Zhang Yafei
"""
from django.core.exceptions import ValidationError
from django.forms import Form
from django.forms import fields
from django.core.validators import RegexValidator
from repository.models import *


class BaseForm(object):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(BaseForm, self).__init__(*args, **kwargs)


class LoginForm(Form):
    """
    登录表单
    """
    def __init__(self,request,*args,**kwargs):
        self.request = request
        super(LoginForm,self).__init__(*args,**kwargs)

    username = fields.CharField()
    pwd = fields.CharField()
    # remember = fields.IntegerField(required=False)
    remember = fields.CheckboxInput()
    check_code = fields.CharField(error_messages={'required':'验证码不能为空'})

    def clean_check_code(self):
        if self.request.session.get('check_code').lower() != self.cleaned_data.get('check_code').lower():
            raise ValidationError(code='invalid',message='验证码错误')
        return self.cleaned_data

    def clean(self):
        username = self.cleaned_data.get('username')
        pwd = self.cleaned_data.get('pwd')
        obj = UserInfo.objects.filter(username=username,pwd=pwd).first()
        if not obj:
            raise ValidationError('用户名或密码错误')
        return self.cleaned_data


class RegisterForm(Form):
    """
    注册表单
    """
    def __init__(self,request,*args,**kwargs):
        self.request = request
        super(RegisterForm,self).__init__(*args,**kwargs)

    username = fields.CharField(min_length=2,max_length=16,
                                error_messages={
                                    'required':'用户名不能为空',
                                    'max_length':'用户名长度不能超过16位字符',
                                    'min_length':'用户名长度不能小于2个字符',
                                })
    pwd = fields.RegexField(regex=r'^(?=.*[A-z])(?=.*\d)(?=.*[#@!~%^&*])[A-z\d#@!~%^&*]{8,16}$',
                            min_length=8,
                            max_length=16,
                            error_messages={
                                'required':'密码不能为空',
                                'invalid':'密码必须包含字母数字和特殊字符',
                                'min_length':'密码长度不能小于8个字符',
                                'max_length':'密码长度不能超过16个字符',
                            },
                            # validators=[RegexValidator(r'^(?=.*[A-z])(?=.*\d)(?=.*[#@!~%^&*])[A-z\d#@!~%^&*]{8,16}$')]
                           )
    pwd2 = fields.CharField()
    email = fields.EmailField(error_messages={'invalid':'请输入正确的邮箱格式'})
    check_code = fields.CharField(error_messages={'required': '验证码不能为空'})

    def clean_check_code(self):
        if self.request.session.get('check_code').lower() != self.cleaned_data.get('check_code').lower():
            raise ValidationError(code='invalid', message='验证码错误')
        return self.cleaned_data['check_code']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        obj = UserInfo.objects.filter(username=username).first()
        if obj:
            raise ValidationError(code='invalid',message='该用户名已注册')
        return self.cleaned_data['username']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        obj = UserInfo.objects.filter(email=email).first()
        if obj:
            raise ValidationError(code='invalid',message='该邮箱已注册')
        return self.cleaned_data['email']

    def clean(self):
        value_dict = self.cleaned_data
        pwd = value_dict.get('pwd')
        pwd2 = value_dict.get('pwd2')
        if pwd != pwd2:
            raise ValidationError('两次密码不一致')
        return self.cleaned_data
