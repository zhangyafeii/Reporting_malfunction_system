# -*- coding: utf-8 -*-

"""
@Datetime: 2018/10/3
@Author: Zhang Yafei
"""
import datetime
import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from backend.forms import TroubleMaker,TroubleKill,TroubleTemp
from repository.models import *
from django.db.models import Q
from django.db import connection
from utils.rbac import permission


@permission
def trouble_list(request,*args,**kwargs):
    user_info = request.session.get('user_info')['id']
    result = Trouble.objects.filter(user=user_info).order_by('status').only('id','title','status','ctime','processor')
    evalute = Trouble.evaluate_choices
    return render(request,'backend_trouble_list.html',{'result':result,'evalute':evalute})


def trouble_detail(request,id):
    obj = Trouble.objects.filter(id=id).first()
    return render(request,'backend_trouble_detail.html',{'obj':obj})


def trouble_create(request):
    if request.method == 'GET':
        form = TroubleMaker()
    else:
        form = TroubleMaker(request.POST)
        if form.is_valid():
            dic = {}
            dic['user_id'] = request.session.get('user_info')['id']
            dic['ctime'] = datetime.datetime.now()
            dic['status'] = 1
            dic.update(form.cleaned_data)
            Trouble.objects.create(**dic)
            return redirect('backend:trouble-list')
    return render(request,'backend_trouble_create.html',{'form':form})


def trouble_edit(request,id):
    if request.method == 'GET':
        obj = Trouble.objects.filter(id=id,status=1).only('id','title','detail').first()
        if not obj:
            return HttpResponse('已处理中的报障单无法修改！')
        #initial，仅仅初始化，不做错误验证
        form = TroubleMaker({'title':obj.title,'detail': obj.detail})
        print(form)
        #执行error会验证
        # return render(request,'backend_trouble_create.html',{'form':form})
        return render(request,'backend_trouble_edit.html',{'form':form,'id':id})
    else:
        form = TroubleMaker(request.POST)
        if form.is_valid():
            v = Trouble.objects.filter(id=id, status=1).update(**form.cleaned_data)
            #v代表受影响的行数，v=1表示更新一条，v=0表示没更新成功，已经被处理
            if not v:
                return HttpResponse('已经被处理')
            else:
                return redirect('backend:trouble-list')
        else:
            return render(request,'backend_trouble_edit.html',{'form':form,'id':id})


def trouble_evalute(request):
    user_id = request.session.get('user_info')['id']
    if request.method == 'POST':
        id = request.POST.get('id')
        evalute = request.POST.get('evalute')
        result = {'status':True,'message':None}
        obj = Trouble.objects.filter(id=id,status=3,evaluate=None,user_id=user_id).first()
        if not obj:
            result['status'] = False
            result['message'] = '已经评价过了！'
            return JsonResponse(result)
        else:
            obj.evaluate = evalute
            obj.save()
            return JsonResponse(result)
    else:
        return redirect('/')


def trouble_del(request):
    result = {'status':True,'message':None}
    id = request.GET.get('id')
    try:
        Trouble.objects.filter(id=id).delete()
    except Exception as e:
        result['status'] = False
        result['message'] = str(e)
    return JsonResponse(result)


@permission
def trouble_kill_list(request,*args,**kwargs):
    user_id = request.session.get('user_info')['id']
    result = Trouble.objects.filter(Q(processor=user_id)|Q(status=1)).order_by('status')
    return render(request,'backend_trouble_kill_list.html',{'result':result})


@permission
def trouble_kill(request,id,*args,**kwargs):
    user_id = request.session.get('user_info')['id']
    temp = TroubleTemplate.objects.filter(user_id=user_id).all()
    if request.method == 'GET':
        ret = Trouble.objects.filter(id=id,processor=user_id).count()
        #以前未抢到
        if not ret:
            v = Trouble.objects.filter(id=id,status=1).update(processor=user_id,status=2,ptime=datetime.datetime.now())
            if not v:
                return HttpResponse('手速太慢！')
        obj = Trouble.objects.filter(id=id).first()
        form = TroubleKill({'title':obj.title,'solution':obj.solution})
        return render(request,'backend_trouble_kill.html',{'form':form,'id':id,'temp':temp})
    else:
        ret = Trouble.objects.filter(id=id, processor=user_id,status=2).count()
        if not ret:
            return HttpResponse('去你妈的')
        form = TroubleKill(request.POST)
        if form.is_valid():
            dic={}
            dic['status'] = 3
            dic['solution'] = form.cleaned_data['solution']
            dic['ptime'] = datetime.datetime.now()
            Trouble.objects.filter(id=id,processor=user_id,status=2).update(**dic)
            return redirect('backend:trouble_kill_list')
        obj = Trouble.objects.filter(id=id).first()
        return render(request,'backend_trouble_kill.html',{'obj':obj,'form':form,'id':id,'temp':temp})


def trouble_kill_del(request):
    user_id = request.session.get('user_info')['id']
    result = {'status':True,'message':None}
    id = request.GET.get('id')
    try:
        Trouble.objects.filter(id=id,processor=user_id,status=2).update(status=1,processor_id=None)
    except Exception as e:
        result['status'] = False
        result['message'] = str(e)
    return JsonResponse(result)


@permission
def trouble_temp_list(request,*args,**kwargs):
    user_id = request.session.get('user_info')['id']
    temp = TroubleTemplate.objects.filter(user_id=user_id).all()
    return render(request,'backend_trouble_temp_list.html',{'temp':temp})


def trouble_temp_create(request):
    user_id = request.session.get('user_info')['id']
    if request.method == 'GET':
        form = TroubleTemp()
    else:
        form = TroubleTemp(request.POST)
        if form.is_valid():
            form.cleaned_data['user_id'] = user_id
            TroubleTemplate.objects.create(**form.cleaned_data)
            return redirect('backend:trouble_temp_list')
    return render(request,'backend_trouble_temp_create.html',{'form':form})


def trouble_temp_edit(request,id):
    user_id = request.session.get('user_info')['id']
    if request.method == 'GET':
        obj = TroubleTemplate.objects.filter(id=id).first()
        form = TroubleTemp(initial={'title':obj.title,'context': obj.context})
        print(form)
        return render(request,'backend_trouble_temp_edit.html',{'form':form,'id':id})
    else:
        form = TroubleTemp(request.POST)
        if form.is_valid():
            TroubleTemplate.objects.filter(id=id,user_id=user_id).update(**form.cleaned_data)
            return redirect('backend:trouble_temp_list')
        else:
            return render(request,'backend_trouble_edit.html',{'form':form,'id':id})


def trouble_temp_del(request):
    result = {'status':True,'message':None}
    id = request.GET.get('id')
    try:
        TroubleTemplate.objects.filter(id=id).delete()
    except Exception as e:
        result['status'] = False
        result['message'] = str(e)
    return JsonResponse(result)


@permission
def trouble_report(request,*args,**kwargs):
    return render(request,'backend_trouble_report.html')


def trouble_json_report(request):
    #数据库中获取数据
    response = []
    user_list = UserInfo.objects.all()
    for user in user_list:
        cursor = connection.cursor()
        cursor.execute("""select strftime('%%s',strftime('%%Y-%%m-01',ptime)) * 1000,count(id) from repository_trouble where processor_id = %s group by strftime('%%Y-%%m',ptime)""",[user.id])
        result = cursor.fetchall()
        # print(user.username,result)
        temp = {
            'name':user.username,
            'data':result,
        }
        response.append(temp)
    return HttpResponse(json.dumps(response))
