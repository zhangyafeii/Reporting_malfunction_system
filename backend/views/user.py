import os
import uuid

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from backend.forms import ArticleForm,UserInfoForm,PasswordForm,NewUserForm,EditUserForm
from repository.models import *
from utils.xss import XSSFilter
from django.db import transaction
from backend.auth.auth import check_login
import base64
from utils.rbac import permission
from utils.pagination import Pagination


@permission
def index(request,*args,**kwargs):
    # action_list = kwargs['action_list']
    # menu_string = kwargs['menu_string']
    user = request.session.get('user_info')
    print(user)
    return render(request, 'backend_index.html')


@check_login
def article(request,**kwargs):
    user_info = request.session.get('user_info')
    blog = Blog.objects.filter(user_id=user_info.get('id')).first()
    type_list = Classification.objects.filter(blog=blog)
    tag_list = Tags.objects.filter(blog=blog)
    condition = {}
    for k, v in kwargs.items():
        kwargs[k] = int(v)
    type_id = kwargs.get('type_id')
    tag_id = kwargs.get('tag_id')
    # print(type_id,tag_id)
    if type_id == 0:
        if tag_id == 0:
            pass
        else:
            condition['tags'] = tag_id
    else:
        if tag_id == 0:
            # Article.objects.filter(blog__classification=type_id)
            pass
        else:
            condition['tags'] = tag_id
        condition['article_classification_id'] = type_id
    condition['blog'] = blog
    # print(condition)
    article_list = Article.objects.filter(**condition).order_by('-publish','-id')
    # article_list = Article.objects.filter(blog=blog,).values('tags','article_classification_id','title')
    data_count = article_list.count()
    page_obj = Pagination(data_count,request.GET.get('p'))
    base_url = reverse('backend:backend_article',kwargs={'type_id':type_id,'tag_id':tag_id})
    page_str = page_obj.page_str(base_url)
    article_list = article_list[page_obj.start:page_obj.end]
    context = {'kwargs':kwargs,'type_list':type_list,
               'tag_list':tag_list,
               'article_list':article_list,
               'data_count':data_count,'page_str':page_str}
    return render(request, 'backend_article.html', context)


@check_login
def edit_article(request,id):
    article_id = id
    blog = request.session['user_info']['blog']
    if request.method == 'GET':
        article = Article.objects.filter(id=article_id).first()
        if not article:
            return render(request, 'backend_no_article.html')
        tags = article.tags.values_list('id')
        if tags:
            tags = list(zip(*tags))[0]
        init_dict = {
            'id':article_id,
            'title':article.title,
            'summary':article.summary,
            'detail':article.detail,
            'article_classification_id':article.article_classification_id,
            'article_type_id':article.article_type_id,
            'tags':tags,
        }
        init_files = {'img':article.img}
        form = ArticleForm(request=request,data=init_dict,files=init_files)
        return render(request, 'backend_edit_article.html', {'form':form, 'id':id})
    elif request.method == 'POST':
        form = ArticleForm(request=request,data=request.POST,files=request.FILES)
        if form.is_valid():
            obj = Article.objects.filter(id=id).first()
            if not obj:
                return render(request, 'backend_no_article.html')
            with transaction.atomic():
                detail = form.cleaned_data.pop('detail')
                detail = XSSFilter().process(detail)
                form.cleaned_data['detail'] = detail
                if 'publish' in request.POST:
                    if obj.publish == 0:
                        form.cleaned_data['publish'] = 1
                tags = form.cleaned_data.pop('tags')
                file = form.cleaned_data['img']
                if file:
                    if not file.name.startswith('static'):
                        form.cleaned_data['img'] = 'static/upload/artcle/'+form.cleaned_data['img'].name
                    if not os.path.exists(form.cleaned_data['img']):
                        f = open(form.cleaned_data['img'],'wb')
                        for row in file.chunks():
                            f.write(row)
                        f.close()
                else:
                    form.cleaned_data.pop('img')
                Article.objects.filter(id=obj.id).update(**form.cleaned_data)
                Ariticle_Tags.objects.filter(article=obj).delete()
                tag_list = []
                for tag_id in tags:
                    tag_id = int(tag_id)
                    tag_list.append(Ariticle_Tags(article_id=obj.id, tag_id=tag_id))
                Ariticle_Tags.objects.bulk_create(tag_list)
            return redirect('/backend/article-0-0.html')
        else:
            return render(request, 'backend_edit_article.html', {'form': form, 'id': id})


@check_login
def add_article(request):
    if request.method == 'GET':
        form = ArticleForm(request=request)
        return render(request, 'backend_add_article.html', {'form':form})
    elif request.method == 'POST':
        form = ArticleForm(request=request, data=request.POST,files=request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            with transaction.atomic():
                detail = form.cleaned_data.pop('detail')
                detail = XSSFilter().process(detail)
                form.cleaned_data['detail'] = detail
                form.cleaned_data['blog_id'] = request.session['user_info']['blog']
                if 'publish' in request.POST:
                    form.cleaned_data['publish'] = 1
                tags = form.cleaned_data.pop('tags')
                obj = Article.objects.create(**form.cleaned_data)
                Ariticle_Tags.objects.filter(article=obj).delete()
                tag_list = []
                for tag_id in tags:
                    tag_id = int(tag_id)
                    tag_list.append(Ariticle_Tags(article_id=obj.id, tag_id=tag_id))
                Ariticle_Tags.objects.bulk_create(tag_list)
            return redirect('/backend/article-0-0.html')
        else:
            return render(request, 'backend_add_article.html', {'form': form})
    else:
        return redirect('/')


@check_login
def del_artcile(request):
    result = {'status':True,'message':None}
    id = request.GET.get('id')
    try:
        Article.objects.filter(id=id).delete()
    except Exception as e:
        result['status'] =False
        result['message'] = str(e)
    return JsonResponse(result)


@permission
def article_classification(request,*args,**kwargs):
    blog_id = request.session['user_info']['blog']
    types = Classification.objects.filter(blog_id=blog_id).all()
    return render(request, 'backend_classification.html', {'types':types})


@check_login
def add_classification(request):
    result = {'status':True,'message':None}
    title = request.POST.get('class_name').strip()
    if title == '':
        result['status'] = False
        result['message'] = '分类信息不能为空'
        return JsonResponse(result)
    blog_id = request.session['user_info']['blog']
    try:
        Classification.objects.create(title=title,blog_id=blog_id)
    except Exception as e:
        result['status'] = False
        result['message'] = str(e)
    return JsonResponse(result)


@check_login
def del_classification(request):
    result = {'status':True,'message':None}
    id = request.GET.get('id')
    print(id)
    try:
        Classification.objects.filter(id=id).delete()
    except Exception as e:
        result['status'] = False
        result['message'] = str(e)
    return JsonResponse(result)


@check_login
def edit_classification(request):
    result = {'status':True,'message':None}
    name = request.POST.get('name')
    id = request.POST.get('id')
    print(name,id)
    try:
        Classification.objects.filter(id=id).update(title=name)
    except Exception as e:
        result['status'] = False
        result['message'] = str(e)
    return JsonResponse(result)


@permission
def article_tag(request,*args,**kwargs):
    blog_id = request.session['user_info']['blog']
    tags = Tags.objects.filter(blog_id=blog_id).all()
    return render(request, 'backend_tag.html', {'tags':tags})


@check_login
def add_tag(request):
    result = {'status': True, 'message': None}
    title = request.POST.get('class_name').strip()
    if title == '':
        result['status'] = False
        result['message'] = '标签信息不能为空'
        return JsonResponse(result)
    # print(request.POST)
    blog_id = request.session['user_info']['blog']
    # print(title)
    try:
        Tags.objects.create(title=title, blog_id=blog_id)
    except Exception as e:
        result['status'] = False
        result['message'] = str(e)
    return JsonResponse(result)


@check_login
def edit_tag(request):
    result = {'status':True,'message':None}
    name = request.POST.get('name')
    id = request.POST.get('id')
    # print(name,id)
    try:
        Tags.objects.filter(id=id).update(title=name)
    except Exception as e:
        result['status'] = False
        result['message'] = str(e)
    return JsonResponse(result)


@check_login
def del_tag(request):
    result = {'status':True,'message':None}
    id = request.GET.get('id')
    print(id)
    try:
        Tags.objects.filter(id=id).delete()
    except Exception as e:
        result['status'] = False
        result['message'] = str(e)
    return JsonResponse(result)


@check_login
def article_images(request):
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

@permission
def personal_view(request,*args,**kwargs):
    user_id = request.session.get('user_info')['id']
    user = UserInfo.objects.filter(id=user_id).first()
    return render(request,'backend_personal_view.html',{'user':user})

@check_login
def my_image(request):
    user = request.session.get('user_info')
    if request.method == 'GET':
        return render(request,'imagecrop.html')
    elif request.method == 'POST':
        img = request.POST.get('img')
        print(type(img))
        img = img.split('base64,')[1]
        images = base64.b64decode(img)
        file_name = str(uuid.uuid1())
        file = open('static/upload/photo/{}.jpg'.format(file_name), 'wb')
        file.write(images)
        file.close()
        photo = os.path.join('static/upload/photo',file_name+'.jpg')
        UserInfo.objects.filter(id=user['id']).update(img=photo)
        request.session.get('user_info')['img'] = photo
        print(request.session.get('user_info')['img'])
        return HttpResponse('1')


@check_login
def personal_update(request):
    user_id = request.session.get('user_info')['id']
    user = UserInfo.objects.filter(id=user_id).first()
    if request.method == 'GET':
        init_dict = {
            'username':user.username,
            'nickname':user.nickname,
            'email':user.email,
        }
        form = UserInfoForm(request=request,data=init_dict)
        return render(request,'backend_personal_update.html',{'form':form,'user':user})
    else:
        form = UserInfoForm(request=request,data=request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            UserInfo.objects.filter(id=user_id).update(**form.cleaned_data)
            return redirect('backend:personal_view')
        else:
            return render(request,'backend_personal_update.html',{'form':form,'user':user})


@permission
def personal_update_pwd(request):
    if request.method == 'GET':
        form = PasswordForm(request=request)
        return render(request,'backend_personal_update_pwd.html',{'form':form})
    else:
        form = PasswordForm(request=request,data=request.POST)
        print(form)
        if form.is_valid():
            pwd = form.cleaned_data['pwd1']
            user_id = request.session.get('user_info')['id']
            UserInfo.objects.filter(id=user_id).update(pwd=pwd)
            return redirect('login')
        return render(request,'backend_personal_update_pwd.html',{'form':form})


@permission
def personal_blog(request,*args,**kwargs):
    user_id = request.session.get('user_info')['id']
    blog = Blog.objects.filter(user_id=user_id).first()
    if request.method == 'GET':
        return render(request,'backend_personal_blog.html',{'blog':blog})
    else:
        render(request, 'backend_personal_update_blog.html')


@permission
def personal_update_blog(request,*args,**kwargs):
    user_id = request.session.get('user_info')['id']
    blog = Blog.objects.filter(user_id=user_id).first()
    # print(blog)
    if request.method == 'GET':
        print('get')
        return render(request,'backend_personal_update_blog.html',{'blog':blog})
    else:
        print('post')
        result = {'status':True,'message':None}
        suffix = request.POST.get('suffix')
        title = request.POST.get('title')
        summary = request.POST.get('summary')
        obj = Blog.objects.filter(suffix=suffix).first()
        if obj:
            if obj.id != blog.id:
                result['status'] = False
                result['message'] = '该前缀已有人使用'
            else:
                blog.suffix = suffix
                blog.title = title
                blog.summary = summary
                blog.save()
        else:
            try:
                Blog.objects.create(user_id=user_id,suffix=suffix,title=title,summary=summary)
            except Exception as e:
                result['status'] = False
                result['message'] = str(e)
        return JsonResponse(result)


@permission
def user_list(request,*args,**kwargs):
    user_list = UserInfo.objects.all()
    page_obj = Pagination(user_list.count(),request.GET.get('p'))
    base_url = reverse('backend:user_list')
    page_str = page_obj.page_str(base_url)
    user_list = user_list[page_obj.start:page_obj.end]
    return render(request,'backend_user_list.html',{'user_list':user_list,'page_str':page_str})


def del_user(request):
    result = {'status':True,'message':None}
    user_id = request.GET.get(('id'))
    try:
        UserInfo.objects.filter(id=user_id).delete()
    except Exception as e:
        result['status'] = False
        result['message'] = str(e)
    return JsonResponse(result)


def add_user(request):
    result = {'status':True,'message':None}
    form = NewUserForm(request=request,data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        UserInfo.objects.create(**form.cleaned_data)
    else:
        result['status'] = False
        result['message'] = form.errors
    return JsonResponse(result)


def edit_user(request):
    result = {'status':True,'message':None}
    form = EditUserForm(request=request,data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        UserInfo.objects.filter(id=form.cleaned_data['id']).update(**form.cleaned_data)
        result['message'] = form.cleaned_data
    else:
        result['status'] = False
        result['message'] = form.errors
    return JsonResponse(result)
