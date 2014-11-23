#coding:utf-8
import re
import random

from django.http.response import HttpResponse as HR
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.db.models import Q
#from django.template import RequestContext

from models import Question,User,Record,Discuss,Vote


# Cron Job
def cron(request):
    pass

#初始化并测试数据库
def test(request):
    user=User.objects.get(username='water33')
    print len(user.password)
    #不同的题型，出现相应不同的模板
    return HR(u'数据库初始化并测试完成')


#生成验证码函数
def verifyimg(request):
    from verify import genImg
    imgbuf,verify_code=genImg()
    request.session['verify_code']=verify_code
    return HR(imgbuf.getvalue(),mimetype='image/gif')


def index(request):
     #如果用户首次进入网页
    if 'user' not in request.session:
        request.session['user'] = u'游客'
        request.session['score']=0
        request.session['degree']=0
        request.session['uid']=0
        request.session['qid']=1
    else:
        pass

    #不同的题型，出现相应不同的模板
    return render_to_response('index.html', {'user':request.session} )



#about
def about(request):
    return render_to_response('about.html', {'user':request.session} )

#help
def help(request):
    return render_to_response('help.html', {'user':request.session} )

