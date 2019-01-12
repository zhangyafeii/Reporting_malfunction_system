from django.db.models import Count, F
from django.http import HttpResponse, Http404, HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from repository.models import *
from django.urls import reverse
from utils.pagination import Pagination
import uuid
from utils.xss import XSSFilter


def index(request,*args,**kwargs):
    """
    网站首页
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    article_type_list = Article.type_choices
    if kwargs:
        article_type_id = int(kwargs['article_type_id'])
        base_url = reverse('index',kwargs={'article_type_id':article_type_id})
    else:
        article_type_id = None
        base_url = '/'
    articlecount = Article.objects.filter(**kwargs).count()
    page_obj = Pagination(articlecount,request.GET.get('p'))
    article_list = Article.objects.filter(**kwargs).order_by('-id')[page_obj.start:page_obj.end]
    page_str = page_obj.page_str(base_url)
    most_read_articles = Article.objects.all().order_by('-read_count')[:7]
    most_like_articles = Article.objects.all().order_by('-up_count')[:7]
    most_comment_articles = Article.objects.order_by('-comment_count')[:7]
    context = {'article_type_list':article_type_list,
               'article_type_id':article_type_id,
               'article_list':article_list,
               'page_str':page_str,'page_obj':page_obj,
               'most_like_articles':most_like_articles,
               'most_read_articles':most_read_articles,
               'most_comment_articles':most_comment_articles,
               }
    return render(request, 'index.html',context)


def home(request,*args,**kwargs):
    """
    个人博客首页
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    blog_site = kwargs['blog_site']
    blog = Blog.objects.filter(suffix=blog_site).select_related('user').first()  #连表查询，只查找一次，加速查询
    if not blog:
        raise Http404
    article_list = Article.objects.filter(blog=blog)
    article_list_count = article_list.count()
    page_obj = Pagination(article_list_count,request.GET.get('p'))
    base_url = reverse(home,kwargs={'blog_site':blog_site})
    page_str = page_obj.page_str(base_url)
    article_list = Article.objects.filter(blog=blog).order_by('-id')[page_obj.start:page_obj.end]
    tag_list = Tags.objects.filter(blog=blog).all()
    classification_list = Classification.objects.filter(blog=blog).all()
    date_list = Article.objects.raw('select id,count(id) as num,strftime("%Y-%m",create_time) as ctime from repository_article where blog_id={} group by strftime("%Y-%m",create_time)'.format(blog.id))
    context = {'blog':blog,'article_list':article_list,
               'tag_list':tag_list,'classification_list':classification_list,
               'date_list':date_list,'page_str':page_str,'page_obj':page_obj}
    return render(request,'home.html',context)


def article_detail(request,blog_site,id):
    """
    文章详情页
    :param request:
    :param blog_site:
    :param id:
    :return:
    """
    article = Article.objects.filter(id=id).first()
    blog = Blog.objects.filter(suffix=blog_site).select_related('user').first()
    article_list = Article.objects.filter(blog=blog).order_by('-id')
    tag_list = Tags.objects.filter(blog=blog).all()
    classification_list = Classification.objects.filter(blog=blog).all()
    date_list = Article.objects.filter(blog=blog).raw(
        'select id,count(id) as num,strftime("%Y-%m",create_time) as ctime from repository_article group by strftime("%Y-%m",create_time)')
    commment_list = Comment.objects.filter(article_id=id)
    commment_list_count = commment_list.count()
    base_url = reverse(article_detail,args=[blog_site,id])
    page_obj = Pagination(commment_list_count,request.GET.get('p'))
    page_str = page_obj.page_str(base_url)
    article.up_count = Article_like_dislike.objects.filter(like=True,article_id=id).count()
    article.down_count = Article_like_dislike.objects.filter(like=False,article_id=id).count()
    context = {'blog': blog, 'article_list': article_list, 'tag_list': tag_list,
               'classification_list': classification_list, 'date_list': date_list,
               'article':article,'comment_list':commment_list,'page_str':page_str,
               'page_obj':page_obj}
    return render(request,'home_article_detail.html',context)


def filter(request,blog_site,condition,value):
    blog = Blog.objects.filter(suffix=blog_site).select_related('user').first()
    if not blog:
        raise Http404
    tag_list = Tags.objects.filter(blog=blog).all()
    classification_list = Classification.objects.filter(blog=blog).all()
    date_list = Article.objects.filter(blog=blog).raw(
        'select id,count(id) as num,strftime("%Y-%m",create_time) as ctime from repository_article group by strftime("%Y-%m",create_time)')
    if condition == 'tag':
        name = Tags.objects.filter(id=value).first().title
        filter_value = '当前标签: {}'.format(name)
        article_list_count = Article.objects.filter(tags=value,blog=blog).all().count()
        page_obj = Pagination(article_list_count,request.GET.get('p'))
        base_url = reverse(filter,kwargs={'blog_site':blog_site,'condition':condition,'value':value})
        page_str = page_obj.page_str(base_url)
        article_list = Article.objects.filter(tags=value,blog=blog)[page_obj.start:page_obj.end]
    elif condition == 'types':
        name = Classification.objects.filter(id=value).first().title
        filter_value = '当前类型: {}'.format(name)
        article_list_count = Article.objects.filter(article_classification=value,blog=blog).all().count()
        page_obj = Pagination(article_list_count,request.GET.get('p'))
        base_url = reverse(filter,kwargs={'blog_site':blog_site,'condition':condition,'value':value})
        print(base_url)
        page_str = page_obj.page_str(base_url)
        article_list = Article.objects.filter(article_classification=value,blog=blog)[page_obj.start:page_obj.end]
    elif condition == 'date':
        filter_value = value
        """mysql"""
        # article_list = models.Article.objects.filter(blog=blog).extra(
        # where=['date_format(create_time,"%%Y-%%m")=%s'], params=[val, ]).all()
        """sqlite"""
        article_list = Article.objects.filter(blog=blog).extra(
            where=['strftime("%%Y-%%m",create_time)=%s'], params=[value, ]).all()  #a = '%s%%'%50
        article_list_count = article_list.count()
        page_obj = Pagination(article_list_count,request.GET.get('p'))
        base_url = reverse(filter,kwargs={'blog_site':blog_site,'condition':condition,'value':value})
        page_str = page_obj.page_str(base_url)
        article_list = article_list[page_obj.start:page_obj.end]
    else:
        article_list = []

    context = {'blog': blog, 'article_list': article_list, 'tag_list': tag_list,
               'classification_list': classification_list, 'date_list': date_list,
               'filter_value':filter_value,'page_str':page_str,'page_obj':page_obj}
    return render(request,'home.html',context)


def comment_images(request):
    img = request.FILES.get('images')
    file_name = str(uuid.uuid1())
    file = open('static/images/{}.jpg'.format(file_name),'wb')
    for row in img.chunks():
        file.write(row)
    file.close()
    result = {
        'error':0,
        'url':'/static/images/{}.jpg'.format(file_name),
        'message':'上传成功'
    }
    return JsonResponse(result)


def submitComment(request):
    result = {'status':True,'message':None}
    if request.method == 'GET':
        article_id = request.GET.get('article_id')
        user_id = request.GET.get('user')
        content = request.GET.get('content').strip()
        content = XSSFilter.process(content)
        # print(content)
        if content == '':
            result['status'] = False
            result['message'] = '评论内容不能为空'
        else:
            try:
                Comment.objects.create(article_id=article_id,comment_user_id=user_id,content=content)
            except Exception as e:
                result['status'] = False
                result['message'] = e
    else:
        article_id = request.POST.get('article_id')
        user_id = request.POST.get('user')
        content = ''.join(request.POST.get('content').split(':')[1:]).strip()
        content = XSSFilter.process(content)
        reply_id = request.POST.get('reply_id')
        if content == '':
            result['status'] = False
            result['message'] = '评论内容不能为空'
        else:
            try:
                Comment.objects.create(article_id=article_id,content=content,comment_user_id=user_id,parent_id_id=reply_id)
                article = Article.objects.filter(article_id=article_id).first()
                article.comment_count = Comment.objects.filter(article_id=article_id).count()
            except Exception as e:
                result['status'] = False
                result['message'] = e
    return JsonResponse(result)


def del_comment(request):
    result = {'status':True,'message':None}
    id = request.POST.get('id')
    print(id)
    try:
        Comment.objects.filter(id=id).delete()
    except Exception as e:
        result['status'] = False
        result['message'] = str(e)
    return JsonResponse(result)


def article_up_or_down(request):
    result = {'status':0,'message':None}
    if request.method == 'GET':
        article_id = request.GET.get('article_id')
        user_id = request.GET.get('user_id')
        if user_id:
            obj = Article_like_dislike.objects.filter(article_id=article_id,user_id=user_id,like=True)
            if obj:
                obj.delete()
                result['status'] = 2
            else:
                try:
                    Article_like_dislike.objects.create(article_id=article_id,user_id=user_id,like=True)
                except Exception as e:
                    result['status'] = 3
                    result['message'] = '只能推荐或反对一次'
        else:
            result['status'] = 1
            result['message'] = '请先登录'
    else:
        article_id = request.POST.get('article_id')
        user_id = request.POST.get('user_id')
        if user_id:
            obj = Article_like_dislike.objects.filter(article_id=article_id,user_id=user_id,like=False)
            if obj:
                obj.delete()
                result['status'] = 2
            else:
                try:
                    Article_like_dislike.objects.create(article_id=article_id,user_id=user_id,like=False)
                except Exception as e:
                    result['status'] = 3
                    result['message'] = '只能推荐或反对一次'
        else:
            result['status'] = 1
            result['message'] = '请先登录'
    return JsonResponse(result)

