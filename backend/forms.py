# -*- coding: utf-8 -*-

"""
@Datetime: 2018/10/2
@Author: Zhang Yafei
"""
from django.core.exceptions import ValidationError
from django.forms import Form
from django.forms import fields
from django.forms import widgets
from repository.models import *


class ArticleForm(Form):

    def __init__(self, request, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        blog_id = request.session['user_info']['blog']
        self.fields['article_classification_id'].choices = Classification.objects.filter(blog_id=blog_id).values_list('id','title')
        self.fields['tags'].choices = Tags.objects.filter(blog_id=blog_id).values_list('id', 'title')

    publish = 0
    title = fields.CharField(widget=widgets.TextInput(attrs={'class':'form-control','placeholder':'文章标题'}))
    summary = fields.CharField(
        widget=widgets.Textarea(attrs={'class': 'form-control', 'placeholder': '文章简介', 'rows': '3'})
    )
    detail = fields.CharField(
        widget=widgets.Textarea(attrs={'class': 'kind-content'})
    )
    # img = fields.ImageField()
    article_type_id = fields.IntegerField(
        widget=widgets.RadioSelect(choices=Article.type_choices)
    )
    article_classification_id = fields.ChoiceField(
        choices=[],
        widget=widgets.RadioSelect
    )
    img = fields.FileField(required=False)
    tags = fields.MultipleChoiceField(
        choices=[],
        widget=widgets.CheckboxSelectMultiple
    )


class TroubleMaker(Form):
    title = fields.CharField(max_length=32,
                             widget=widgets.TextInput(attrs={'class':'form-control'})
                             )
    detail = fields.CharField(
        widget=widgets.Textarea(attrs={'id':'detail','class':'kind-editor'})
    )


class TroubleKill(Form):
    title = fields.CharField(max_length=32,
                             widget=widgets.TextInput(attrs={'class':'form-control','readonly':'readonly'})
                             )
    solution = fields.CharField(
        widget=widgets.Textarea(attrs={'id':'solution','class':'kind-editor'})
    )


class TroubleTemp(Form):
    title = fields.CharField(max_length=32,
                             widget=widgets.TextInput(attrs={'class':'form-control'})
                             )
    context = fields.CharField(
        widget=widgets.Textarea(attrs={'id':'context','class':'kind-editor'})
    )


class UserInfoForm(Form):

    def __init__(self, request, *args, **kwargs):
        super(UserInfoForm, self).__init__(*args, **kwargs)
        self.user = request.session.get('user_info')

    username = fields.CharField(min_length=2, max_length=16,
                                widget=widgets.TextInput(attrs={'class':'form-control'}),
                                error_messages={
                                    'required': '用户名不能为空',
                                    'max_length': '用户名长度不能超过16位字符',
                                    'min_length': '用户名长度不能小于2个字符',
                                })
    nickname = fields.CharField(min_length=2, max_length=16,
                                widget=widgets.TextInput(attrs={'class':'form-control'}),
                                error_messages={
                                    'required': '昵称不能为空',
                                    'max_length': '用户名长度不能超过16位字符',
                                    'min_length': '用户名长度不能小于2个字符',
                                })
    email = fields.EmailField(error_messages={'invalid': '请输入正确的邮箱格式'},
                              widget=widgets.TextInput(attrs={'class':'form-control'}),
                            )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        print(username)
        obj = UserInfo.objects.filter(username=username).first()
        if obj and obj.id != self.user['id']:
            raise ValidationError(code='invalid',message='该用户名已注册')
        return self.cleaned_data['username']

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        print(nickname)
        obj = UserInfo.objects.filter(nickname=nickname).first()
        if obj and obj.id != self.user['id']:
            raise ValidationError(code='invalid',message='该昵称已被注册')
        return self.cleaned_data['nickname']


class PasswordForm(Form):
    def __init__(self, request, *args, **kwargs):
        super(PasswordForm, self).__init__(*args, **kwargs)
        self.user = request.session.get('user_info')

    pwd = fields.CharField(widget=widgets.PasswordInput(attrs={'class':'form-control'}))
    pwd1 = fields.RegexField(regex=r'^(?=.*[A-z])(?=.*\d)(?=.*[#@!~%^&*])[A-z\d#@!~%^&*]{8,16}$',
                            min_length=8,
                            max_length=16,
                            error_messages={
                                'required': '密码不能为空',
                                'invalid': '密码必须包含字母数字和特殊字符',
                                'min_length': '密码长度不能小于8个字符',
                                'max_length': '密码长度不能超过16个字符',
                            },
                             widget=widgets.PasswordInput(attrs={'class':'form-control'}),
                            # validators=[RegexValidator(r'^(?=.*[A-z])(?=.*\d)(?=.*[#@!~%^&*])[A-z\d#@!~%^&*]{8,16}$')]
                            )
    pwd2 = fields.CharField(widget=widgets.PasswordInput(attrs={'class':'form-control'}))

    def clean_pwd(self):
        if self.cleaned_data.get('pwd') != self.user['pwd']:
            raise ValidationError('原密码不正确！')
        return self.cleaned_data['pwd']

    def clean(self):
        value_dict = self.cleaned_data
        pwd1 = value_dict.get('pwd1')
        pwd2 = value_dict.get('pwd2')
        if pwd1 != pwd2:
            raise ValidationError('两次密码不一致')
        return self.cleaned_data


class NewUserForm(Form):
    """
    新用户表单
    """
    def __init__(self,request,*args,**kwargs):
        self.request = request
        super(NewUserForm,self).__init__(*args,**kwargs)

    username = fields.CharField(min_length=2,max_length=16,
                                error_messages={
                                    'required':'用户名不能为空',
                                    'max_length':'用户名长度不能超过16位字符',
                                    'min_length':'用户名长度不能小于2个字符',
                                })
    nickname = fields.CharField(max_length=32,min_length=2,
                                error_messages={
                                    'required':'用户名不能为空',
                                    'max_length':'用户名长度不能超过32位字符',
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
                            })
    email = fields.EmailField(error_messages={'invalid':'请输入正确的邮箱格式'})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        obj = UserInfo.objects.filter(username=username).first()
        if obj:
            raise ValidationError(code='invalid',message='该用户名已注册')
        return self.cleaned_data['username']

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        obj = UserInfo.objects.filter(nickname=nickname).first()
        if obj:
            raise ValidationError(code='invalid',message='该用户名已注册')
        return self.cleaned_data['nickname']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        obj = UserInfo.objects.filter(email=email).first()
        if obj:
            raise ValidationError(code='invalid',message='该邮箱已注册')
        return self.cleaned_data['email']


class EditUserForm(Form):
    """
    编辑用户表单
    """
    def __init__(self,request,*args,**kwargs):
        self.request = request
        super(EditUserForm,self).__init__(*args,**kwargs)
    id = fields.IntegerField()
    username = fields.CharField(min_length=2,max_length=16,
                                error_messages={
                                    'required':'用户名不能为空',
                                    'max_length':'用户名长度不能超过16位字符',
                                    'min_length':'用户名长度不能小于2个字符',
                                })
    nickname = fields.CharField(max_length=32,min_length=2,
                                error_messages={
                                    'required':'用户名不能为空',
                                    'max_length':'用户名长度不能超过32位字符',
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
                            })
    email = fields.EmailField(error_messages={'invalid':'请输入正确的邮箱格式'})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        obj = UserInfo.objects.filter(username=username).first()
        if obj and obj.id != self.cleaned_data['id']:
            raise ValidationError(code='invalid',message='该用户名已注册')
        return self.cleaned_data['username']

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        obj = UserInfo.objects.filter(nickname=nickname).first()
        if obj and obj.id != self.cleaned_data['id']:
            raise ValidationError(code='invalid',message='该昵称已注册')
        return self.cleaned_data['nickname']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        obj = UserInfo.objects.filter(email=email).first()
        if obj and obj.id != self.cleaned_data['id']:
            raise ValidationError(code='invalid',message='该邮箱已注册')
        return self.cleaned_data['email']


