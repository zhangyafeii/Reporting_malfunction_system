# -*- coding: utf-8 -*-

"""
@Datetime: 2018/9/20
@Author: Zhang Yafei
"""
from django.utils.safestring import mark_safe


class Pagination(object):
    def __init__(self,total_count,current_page,per_page_num=10,max_page_num=7):
        #数据总个数
        self.total_count = total_count
        #当前页
        try:
            v = int(current_page)
            if v <= 0:
                v = 1
            self.current_page = v
        except:
            self.current_page = 1
        #每页显示的行数
        self.per_page_num = per_page_num
        #每页显示的最多页码
        self.max_page_num = max_page_num

    @property
    def start(self):
        return (self.current_page-1) * self.per_page_num

    @property
    def end(self):
        return self.current_page * self.per_page_num

    @property
    def num_pages(self):
        """
        总页数
        :return:
        """
        a,b = divmod(self.total_count,self.per_page_num)
        if b == 0:
            return a
        return a+1

    def pager_num_range(self):
        if self.num_pages < self.max_page_num:
            return range(1, self.num_pages + 1)
        # 总页数特别多
        part = int(self.max_page_num / 2)
        if self.current_page < part:
            return range(1, self.max_page_num + 1)
        if (self.current_page + part) > self.num_pages:
            return range(self.current_page - self.max_page_num + 1, self.num_pages + 1)
        return range(self.current_page - part, self.current_page + part + 1)

    def page_str(self,base_url):
        page_list = []

        first = '<li><a href="{}?p=1">首页</a></li>'.format(base_url)
        page_list.append(first)

        if self.current_page == 1:
            prev = '<li><a href="#">上一页</a></li>'
        else:
            prev = '<li><a href="{0}?p={1}">上一页</a></li>'.format(base_url,self.current_page-1)
        page_list.append(prev)
        for i in self.pager_num_range():
            if i == self.current_page:
                temp = '<li class="active"><a href="{0}?p={1}">{2}</a></li>'.format(base_url,i,i)
            else:
                temp = '<li><a href="{0}?p={1}">{2}</a></li>'.format(base_url,i, i)
            page_list.append(temp)
        if self.current_page == self.num_pages:
            next = '<li><a href="#">下一页</a></li>'
        else:
            next = '<li><a href="{0}?p={1}">下一页</a></li>'.format(base_url,self.current_page + 1)
        page_list.append(next)

        end = '<li><a href="{0}?p={1}">尾页</a></li>'.format(base_url,self.num_pages)
        page_list.append(end)

        return mark_safe(''.join(page_list))