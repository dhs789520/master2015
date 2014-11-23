#coding:utf-8
import re
import random

from django.http.response import HttpResponse as HR
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.db.models import Q
#from django.template import RequestContext

from models import Question,User,Record,Discuss,Vote

from view.user import *

def init(request):
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
    return HR(imgbuf.getvalue(),'image/gif')


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

#显示答案及解析
def showAnswer(request):
    if request.session['score']==0:
        return HR(u'需要登录后才可以查看答案及解析！')
    else:
        return HR(request.session['answer']+request.session['explain'])


#提交讨论投票
def vote(request):
    if request.session['score']==0:
        return HR(u'需要登录后才可以投票！')
    else:
        did=request.POST['did']
        score=request.POST['score']
         #查询是否已投票此(did)discussid
        if Vote.objects.filter(user_id=request.session['uid'],discuss_id=did).count()==1:
            return HR(u'亲，只能投票一次噢！')

        d=Discuss.objects.get(id=did)

        if d.user_id==request.session['uid']:
            return HR(u'亲，不可以为自己投票的哦！')

        #更新vote表
        v=Vote()
        v.user_id=request.session['uid']
        v.discuss_id=did
        v.vote =score
        v.save()
        #更新用户表，增加score
        u=User.objects.get(id=d.user_id)

        if score=='1':
            d.support +=1
            u.score+=1
        else:
            d.oppose +=1
            u.score-=1
            if u.score <1:
                u.score=1
        d.save()
        u.save()
        
        return HR(u'success')

#显示题目
def showQuestion(request):
    q=Question.objects.filter(id=request.session['qid'])[0]
    #u=User.objects.filter(id=request.session['uid'])[0]
    #request.session['qid']=q.id
     #记录日志
    record=Record()
    record.uid=request.session['uid']
    record.qid=request.session['qid']
    record.result=True
    record.save()

    request.session['answer']=q.answer
    request.session['explain']=q.qexplain

    # 显示最新的和最热的几条讨论
    discuss_new=Discuss.objects.filter(qid=request.session['qid']).order_by('-date')[0:10]
    discuss_hot=Discuss.objects.filter(qid=request.session['qid']).order_by('-support')[0:10]

    #增加一个随机验证码
    if random.randint(1,80)==2:
        request.session['next_verify']=2
    #不同的题型，出现相应不同的模板
    return render_to_response('question_with_base.html', {'q' : q,\
            'includeQuestion':'question%d.html'%(q.qtype),'user':request.session,\
            'discuss_new':discuss_new,'discuss_hot':discuss_hot} )

#讨论
def discuss(request):
    content=request.POST['content']
    if len(content)<10 or len(content)>1000:
        return HR(u'讨论内容违规')

    discuss=Discuss()
    discuss.content=content
    discuss.user_id=request.session['uid']
    discuss.qid=request.session['qid']
    discuss.save()
    return HttpResponseRedirect('/showQuestion')

#带验证功能的下一题
def next_verify(request):
    if 'next_verify' in request.session and request.session['next_verify'] ==2:
        del(request.session['next_verify'])
        print 'success1'
        #验证成功，进入下一题
        return next(request)
    else:
        del(request.session['next_verify'])
        return HR(u'亲，不要爬我的小站了！')


def next(request):
    print 'success3'
    request.session['qid'] +=1
    if request.session['uid'] ==0 and request.session['qid'] >50:
        return HR(u'亲，请先登录，游客只能浏览前50题！')

    if 'next_verify' in request.session and request.session['next_verify']==2:
        return HR(u'亲，不要爬我的小站了！')

    #如果存在用户uid !=0 ，即非游客
    if request.session['uid']:
        user= User.objects.filter(id=request.session['uid'])[0]
        user.qid=request.session['qid']
        user.save()
    return HttpResponseRedirect('/showQuestion')

    #不同的题型，出现相应不同的模板
    return render_to_response('question_with_base.html', {'q' : q,\
            'includeQuestion':'question%d.html'%(q.qtype),'user':request.session} )


def pre(request):
    request.session['qid'] -=1
     #如果存在用户id !=0
    if request.session['uid']:
        user= User.objects.filter(id=request.session['uid'])[0]
        user.qid=request.session['qid']
        user.save()
    return HttpResponseRedirect('/showQuestion')

    #不同的题型，出现相应不同的模板
    return render_to_response('question_with_base.html', {'q' : q,'includeQuestion':'question%d.html'%(q.qtype)} )

def jump(request):
    id= request.GET.get('id','')
    if not re.match('^\d+$',id):
        return HttpResponseRedirect('/')

    request.session['id'] = id
    
    q=Question.objects.get(id=id)
    request.session['id']=q.id
    #不同的题型，出现相应不同的模板
    return render_to_response('question_with_base.html', {'q' : q,'includeQuestion':'question%d.html'%(q.qtype)} )


def search(request):
    keyword= request.POST.get('keyword','')
    if keyword =='':
        return HR(u'Error: 空的搜索词！')

    area= request.POST.get('area','')
    
    if area == u'仅题目':
        questions=Question.objects.filter(question__contains = keyword)
    elif area == u'全部内容':
        questions=Question.objects.filter(Q(question__contains = keyword)|
                    Q(a__contains = keyword)|
                    Q(b__contains = keyword)|
                    Q(c__contains = keyword)|
                    Q(d__contains = keyword)|
                    Q(e__contains = keyword)|
                    Q(content__contains = keyword)|
                    Q(qexplain__contains = keyword)
                    )
    
    #不同的题型，出现相应不同的模板
    return render_to_response('searchResult.html', {'questions' : questions ,'search_keyword':keyword} )


#直接根据qid定位question
def locateQuestion(request,id):
    if not re.match('^\d+$',id):
        return HttpResponseRedirect('/')

    request.session['id'] = id
    
    q=Question.objects.get(id=id)
    #不同的题型，出现相应不同的模板
    return render_to_response('question_without_base.html', {'q' : q,'includeQuestion':'question%d.html'%(q.qtype)} )



