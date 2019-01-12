#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def tag_all(arg_dict):
    type_id = arg_dict['type_id']
    tag_id = arg_dict['tag_id']
    p = arg_dict['p']
    base_url = reverse('backend:backend_article', kwargs={'type_id': type_id, 'tag_id':0 })
    if tag_id == '0':
        temp = '<a class="active" href="%s?p=%s">全部</a>' % (base_url,p,)
    else:
        temp = '<a href="%s?p=%s">全部</a>' % (base_url,p,)
    return mark_safe(temp)


@register.simple_tag
def tag_combine(obj_list, arg_dict):
    li = []
    type_id = arg_dict['type_id']
    tag_id = arg_dict['tag_id']
    p = arg_dict['p']
    for obj in obj_list:
        url = reverse('backend:backend_article', kwargs={'type_id': type_id, 'tag_id': obj['id']})
        if obj['id'] == int(tag_id):
            temp = '<a class="active" href="%s?p=%s">%s</a>' % (url,p, obj['title'])
        else:
            temp = '<a href="%s?p=%s">%s</a>' % (url,p, obj['title'])
        li.append(temp)
    return mark_safe(''.join(li))


@register.simple_tag
def article_type_all(arg_dict):
    type_id = arg_dict['type_id']
    tag_id = arg_dict['tag_id']
    p = arg_dict['p']
    url = reverse('backend:backend_article', kwargs={'type_id': 0, 'tag_id': tag_id})
    if type_id == '0':
        temp = '<a class="active" href="%s?p=%s">全部</a>' % (url,p,)
    else:
        temp = '<a href="%s?p=%s">全部</a>' % (url,p,)
    return mark_safe(temp)


@register.simple_tag
def article_type_combine(obj_list, arg_dict):
    li = []
    type_id = arg_dict['type_id']
    tag_id = arg_dict['tag_id']
    p = arg_dict['p']
    for obj in obj_list:
        url = reverse('backend:backend_article', kwargs={'type_id': obj['id'], 'tag_id': tag_id})
        if obj['id'] == int(type_id):
            temp = '<a class="active" href="%s?p=%s">%s</a>' % (url,p, obj['title'])
        else:
            temp = '<a href="%s?p=%s">%s</a>' % (url,p, obj['title'])
        li.append(temp)
    return mark_safe(''.join(li))