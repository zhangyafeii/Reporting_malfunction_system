# -*- coding: utf-8 -*-

"""
@Datetime: 2018/9/26
@Author: Zhang Yafei
"""
from io import BytesIO

from django.shortcuts import *
from utils.pagination import Pagination
from utils.rbac import PermissionHelper
from web.forms import LoginForm,RegisterForm
from repository.models import *
from django.http import JsonResponse
from utils.check_code import create_validate_code


def login(request):
    """
    用户登录
    1.ajax发送请求
    2.表单验证用户名密码合法性
    3.若验证合法，且选中记住单选框，设置session保持登录状态
    4.将验证结果返回到前端
    :param request:
    :return:
    """
    if request.method =='GET':
        return render(request,'login.html')
    else:
        result = {'status':False,'errors':None}
        form = LoginForm(request=request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('pwd')
            user_info = UserInfo.objects.filter(username=username,pwd=pwd).values('id','nickname','pwd','username','email','img','blog','blog__suffix',).first()
            result['status'] = True
            request.session['user_info'] = user_info
            PermissionHelper(request, username, pwd)
            if form.cleaned_data.get('remember'):
                request.session.set_expiry(60 * 60 * 24 * 30)
        else:
            result['errors'] = form.errors
        return JsonResponse(result)


def register(request):
    """
    用户注册，
    1.通过ajax发送请求
    2.后台通过表单验证用户名密码的合法性
    3.将验证结果返回前端
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        result = {'status':False,'errors':None}
        value_dict = RegisterForm(request=request,data=request.POST)
        if value_dict.is_valid():
            result['status'] = True
            username = value_dict.cleaned_data.get('username')
            pwd = value_dict.cleaned_data.get('pwd')
            email = value_dict.cleaned_data.get('email')
            UserInfo.objects.create(username=username,pwd=pwd,email=email)
            print('注册成功！')
        else:
            result['errors'] = value_dict.errors
        return JsonResponse(result)


def logout(request):
    """
    直接通过删除request.session['user_info]返回的时候，
    如果user_info对应的value值不存在会导致程序异常。所以
    需要做异常处理
    """
    try:
        # 删除is_login对应的value值
        #del request.session['user_info']
        request.session.clear()
    except KeyError:
        pass
    # 点击注销之后，直接重定向回登录页面
    return redirect('/')


def check_code(request):
    """
    测试用：检测验证码
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request,'check_code.html')
    else:
        input_code = request.POST.get('code').lower()
        code = request.session['check_code'].lower()
        print(input_code)
        print(code)
        return HttpResponse('恭喜你，验证通过')


def get_check_code(request):
    """
    生成验证码图片
    :param request:
    :return:
    """
    img,code = create_validate_code()
    file = BytesIO()  #存到内存
    img.save(file,'PNG')
    request.session['check_code'] = code
    return HttpResponse(file.getvalue())

