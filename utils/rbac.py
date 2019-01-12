# -*- coding: utf-8 -*-

"""
@Datetime: 2018/10/6
@Author: Zhang Yafei
"""

from django.shortcuts import HttpResponse, redirect
from repository.models import *
import re


class PermissionHelper(object):
    def __init__(self,request,username,pwd):
        #当前请求的request对象
        self.request = request
        #当前用户名
        self.username = username
        self.pwd = pwd
        #获取当前url
        self.current_url = request.path_info
        # 获取当前用户的所有权限
        self.permissiontoaction_dict = None
        # 获取在菜单中显示的权限
        self.menu_leaf_list = None
        #获取所有菜单
        self.menu_list = None
        # 放在session中
        self.session_data()

    def session_data(self):
        permission_dict = self.request.session.get('permission_info')
        if permission_dict:
            self.permissiontoaction_dict = permission_dict['permissiontoaction_dict']
            self.menu_leaf_list = permission_dict['menu_leaf_list']
            self.menu_list = permission_dict['menu_list']
        else:
        # ===========>获取当前用户角色列表<===============
            role_list = Role.objects.filter(userinfotorole__user__username=self.username, userinfotorole__user__pwd=self.pwd)
            # ###############获取当前用户权限列表(url+action)###############
            # v = [
            #     {'url':'index.html','code':'get'},
            #     {'url':'order.html','code':'get'},
            #     {'url':'order.html','code':'get'},
            #     {'url':'index.html','code':'get'},
            # ]
            # v = {'index.html':['get'.'post']}
            # 获取个人所有权限列表，放置在session中，缺点：无法实时获取权限信息，需重新登录
            permissiontoaction_list = PermissionToAction.objects. \
                filter(roletopremissiontoaction__role__in=role_list). \
                values('permission__url', 'action__code').distinct()

            permissiontoaction_dict = {}
            for item in permissiontoaction_list:
                if item['permission__url'] in permissiontoaction_dict:
                    permissiontoaction_dict[item['permission__url']].append(item['action__code'])
                else:
                    permissiontoaction_dict[item['permission__url']] = [item['action__code'],]

            #获取菜单的叶子节点，即：菜单中在最后一层显示的权限
            menu_leaf_list = list(PermissionToAction.objects. \
                filter(roletopremissiontoaction__role__in=role_list). \
                exclude(permission__menu__isnull=True). \
                values('permission_id', 'permission__url', 'permission__caption', 'permission__menu').distinct())
            #获取所有的菜单列表
            menu_list = list(Menu.objects.values('id', 'caption', 'parent_id'))
            self.request.session['permission_info'] = {
                'permissiontoaction_dict':permissiontoaction_dict,
                'menu_leaf_list':menu_leaf_list,
                'menu_list':menu_list,
            }

    def actions(self):
        """
        检查当前用户是否对当前URL有权访问，并获取当前url有什么权限
        :return:
        """
        action_list = []
        #当前所有权限
        for k,v in self.permissiontoaction_dict.items():
            if re.match(k,self.current_url):
                action_list = v
                break

        return action_list

    def menu_data_list(self):
        menu_leaf_dict = {}
        open_leaf_parent_id = None
        for item in self.menu_leaf_list:
            item = {
                'id': item['permission_id'],
                'url': item['permission__url'],
                'caption': item['permission__caption'],
                'parent_id': item['permission__menu'],
                'child': [],
                'status': True,
                'open': False,
            }
            if item['parent_id'] in menu_leaf_dict:
                menu_leaf_dict[item['parent_id']].append(item)
            else:
                menu_leaf_dict[item['parent_id']] = [item, ]

            if re.match(item['url'], self.current_url):
                item['open'] = True
                open_leaf_parent_id = item['parent_id']

        # 获取所有菜单字典
        menu_dict = {}
        for item in self.menu_list:
            item['child'] = []
            item['status'] = False
            item['open'] = False
            menu_dict[item['id']] = item

        # 将叶子结点添加到菜单中
        for k, v in menu_leaf_dict.items():
            menu_dict[k]['child'] = v
            parent_id = k
            #将后代中有叶子结点的菜单标记为显示
            while parent_id:
                menu_dict[parent_id]['status'] = True
                parent_id = menu_dict[parent_id]['parent_id']

        while open_leaf_parent_id:
            menu_dict[open_leaf_parent_id]['open'] = True
            open_leaf_parent_id = menu_dict[open_leaf_parent_id]['parent_id']

        #########处理等级关系#######
        # menu_dict:应用：评论（xx.objects.values())
        #生成树形结构
        result = []
        for row in menu_dict.values():
            if not row['parent_id']:
                result.append(row)
            else:
                menu_dict[row['parent_id']]['child'].append(row)
        return result

    def menu_content(self,content):
        tpl = """ 
             <div class="item">
                 <div class="item-title"><i class="fa fa-cogs" aria-hidden="true"></i>{0}</div>
                 <div class="item-content">{1}</div>
             </div>
             """
        response = ""
        for row in content:
            active = ""
            if not row['status']:
                continue
            if row['open']:
                active = 'active'
            if 'url' in row:
                response += '<a href="{0}">{1}</a>'.format(row['url'], row['caption'])
            else:
                title = row['caption']
                content = self.menu_content(row['child'])
                response += tpl.format(title, content)
        return response

    def menu_tree(self):
        tpl = """ 
            <div class="item">
                <div class="item-title"><i class="fa fa-cogs" aria-hidden="true"></i>{0}</div>
                <div class="item-content">{1}</div>
            </div>
            """
        response = ""
        for row in self.menu_data_list():
            active = ""
            if not row['status']:
                continue
            if row['open']:
                active = "active"
            # 第一层第一个
            title = row['caption']
            # 第一层第一个后代
            content = self.menu_content(row['child'])
            response += tpl.format(title, content)
        return response


def permission(func):
    def inner(request,*args,**kwargs):
        user_info = request.session.get('user_info')
        if not user_info:
            return redirect('/login.html')
        obj = PermissionHelper(request, user_info['username'], user_info['pwd'])
        action_list = obj.actions()
        if not action_list:
            return HttpResponse('无权限访问')
        menu_string = obj.menu_tree()
        kwargs['action_list'] = action_list
        kwargs['menu_string'] = menu_string
        return func(request,*args,**kwargs)
    return inner
