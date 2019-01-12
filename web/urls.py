# -*- coding: utf-8 -*-

"""
@Datetime: 2018/9/25
@Author: Zhang Yafei
"""
from django.conf.urls import url
from web.views import home,account

urlpatterns = [
    url(r'^$', home.index),
    url(r'^all/(?P<article_type_id>\d+).html$', home.index, name='index'),
    url(r'^login.html$',account.login,name='login'),
    url(r'^register.html$',account.register,name='register'),
    url(r'^logout.html$',account.logout,name='logout'),
    url(r'^check_code.html',account.check_code,name='check_code'),
    url(r'^get_check_code',account.get_check_code,name='get_check_code'),
    url(r'^comment_images.html$',home.comment_images,name='comment_images'),
    url(r'^submitComment$',home.submitComment,name='submitComment'),
    url(r'^del_comment$',home.del_comment,name='del_comment'),
    url(r'^article_up_or_down',home.article_up_or_down,name='article_up_or_down'),
    url(r'^(?P<blog_site>\w+)/(?P<condition>((date)|(types)|(tag)))/(?P<value>\w+-*\w*).html$',home.filter,name='filter'),
    url(r'^(?P<blog_site>\w+).html$',home.home,name='home'),
    url(r'^(\w+)/(\d+).html$',home.article_detail,name='article_detail'),
]