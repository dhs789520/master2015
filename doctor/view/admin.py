#coding:utf-8
# 管理员操作表
# 其中注意 导入模块方式发生改变  from doctor.models 而不是直接 from models
import re
import random

from django.http.response import HttpResponse as HR
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.db.models import Q
#from django.template import RequestContext


from doctor.models import Question,User,Record,Discuss,Vote

#生成验证码图片
def verifyimg(request):
    from verify import genImg
    imgbuf,verify_code=genImg()
    request.session['verify_code']=verify_code
    return HR(imgbuf.getvalue(),'image/gif')

#用户登录
def admin_login(request):
     #如果GET则显示login_form页面
    if request.method == 'GET':
        return render_to_response('login_form.html')

     #如果POST数据，则处理数据
    elif request.method =='POST':
        username=request.POST['username']
        password=request.POST['password'] 
        verify=request.POST['verify']

        error=[]
         #如果验证码错误
        if request.session['verify_code'].lower() != verify.lower():
            error.append(u'验证码输入错误')

        user= User.objects.filter(username=username,password=password)
         #验证用户名及密码
        if user.count()<1:
            error.append(u'用户名或密码错误')
         #输入出错，返回登录页面，提示出错信息
        if error:
            loginfo={'username':username,'password':password}
            return render_to_response('login_form.html',{'error':error,'loginfo':loginfo})

        
        
         #设置session
        request.session['user']=user[0].username
        request.session['score']=user[0].score
        request.session['degree']=user[0].degree
        request.session['uid']=user[0].id
        request.session['qid']=user[0].qid
        return render_to_response('login_success.html')


#退出登录
def admin_logout(request):
     #设置session
    request.session['user']='游客'
    request.session['score']=0
    request.session['degree']=0
    request.session['qid']=1
    request.session['uid']=0
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))







