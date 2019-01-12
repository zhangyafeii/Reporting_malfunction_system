# -*- coding: utf-8 -*-

"""
@Datetime: 2018/9/30
@Author: Zhang Yafei
"""
from django.conf.urls import url
from backend.views import user,trouble

app_name = 'backend'

urlpatterns = [
    url(r'^index.html$', user.index, name='backend_index'),
    url(r'^article-(?P<type_id>\d+)-(?P<tag_id>\d+).html$', user.article, name='backend_article'),
    url(r'^edit_article-(\d+).html$', user.edit_article, name='backend_edit_article'),
    url(r'^add_article.html$', user.add_article, name='backend_add_article'),
    url(r'^del_article.html$', user.del_artcile, name='backend_del_article'),
    url(r'article_classification.html', user.article_classification, name='article_classification'),
    url(r'^add_classification$', user.add_classification, name='add_classification'),
    url(r'^del_classification$', user.del_classification, name='del_classification'),
    url(r'^edit_classification$', user.edit_classification, name='edit_classification'),
    url(r'^article_tag.html', user.article_tag, name='article_tag'),
    url(r'^add_tag$', user.add_tag, name='add_tag'),
    url(r'^edit_tag$', user.edit_tag, name='edit_tag'),
    url(r'^del_tag$', user.del_tag, name='del_tag'),
    url(r'^article_images$', user.article_images, name='article_images'),

    #一般用户：提交报障单，查看，修改（未处理状态），评分（处理完成，未评分）
    url(r'^trouble-list$',trouble.trouble_list,name='trouble-list'),
    url(r'^trouble-create$',trouble.trouble_create,name='trouble_create'),
    url(r'^trouble-edit-(\d+)$',trouble.trouble_edit,name='trouble_edit'),
    url(r'^trouble-del$',trouble.trouble_del,name='trouble_del'),
    url(r'^trouble-detail-(\d+)$',trouble.trouble_detail,name='trouble_detail'),
    url(r'^trouble-evalute$',trouble.trouble_evalute,name='trouble_evalute'),

    url(r'^trouble-kill-list$',trouble.trouble_kill_list,name='trouble_kill_list'),
    url(r'^trouble-kill-(\d+)$',trouble.trouble_kill,name='trouble_kill'),
    url(r'^trouble-kill-del$',trouble.trouble_kill_del,name='trouble_kill_del'),

    url(r'^trouble-temp-list$',trouble.trouble_temp_list,name='trouble_temp_list'),
    url(r'^trouble-temp-create$',trouble.trouble_temp_create,name='trouble_temp_create'),
    url(r'^trouble-temp-edit-(\d+)$',trouble.trouble_temp_edit,name='trouble_temp_edit'),
    url(r'^trouble-temp-del$',trouble.trouble_temp_del,name='trouble_temp_del'),

    url(r'^trouble-report$',trouble.trouble_report,name='trouble_report'),
    url(r'^trouble-json-report$',trouble.trouble_json_report,name='trouble_json_report'),

    url(r'^personal-view.html$',user.personal_view,name='personal_view'),
    url(r'^personal-update.html$',user.personal_update,name='personal_update'),
    url(r'^personal-update-pwd.html$',user.personal_update_pwd,name='personal_update_pwd'),
    url(r'^personal-blog.html$',user.personal_blog,name='personal_blog'),
    url(r'^personal-update-blog.html$',user.personal_update_blog,name='personal_update_blog'),
    url(r'^my_image$',user.my_image,name='my_image'),

    url(r'^user-list$',user.user_list,name='user_list'),
    url(r'^del-user$',user.del_user,name='del_user'),
    url(r'^add-user$',user.add_user,name='add_user'),
    url(r'^edit-user$',user.edit_user,name='edit_user'),
]