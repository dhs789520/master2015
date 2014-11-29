#coding:utf-8
import re
import random

from django.http.response import HttpResponse as HR
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.db.models import Q
#from django.template import RequestContext

from doctor.models import Question,User,Record,Discuss,Vote,Qstore




#生成验证码函数
def verifyimg(request):
    from verify import genImg
    imgbuf,verify_code=genImg()
    request.session['verify_code']=verify_code
    return HR(imgbuf.getvalue(),'image/gif')



#显示答案及解析
def showAnswer(request,answer):
    if request.session['degree']==0:
        return HR(u'需要登录后才可以查看答案及解析！')

    if answer==request.session['answer'] and len(answer)>1:
        return HR("<font color=blue>√  恭喜你，答案正确!</font>：%s<br>%s"%(request.session['answer'],request.session['explain']))
    elif answer != request.session['answer'] and len(answer)>1:
        return HR("<font color=red>X 答案错误</font><br>正确答案：%s<br>%s"%(request.session['answer'],request.session['explain']))
    else:
        return HR("正确答案：%s<br>%s"%(request.session['answer'],request.session['explain']))



#显示题目
def showQuestion(request):

    if 'username' not in request.session:
        return HttpResponseRedirect('/')

    q=Question.objects.filter(id=request.session['qid'])[0]
    if not q:
        return HR('没有此数据')

    #如果此题已经被收藏
    if Qstore.objects.filter(question_id=request.session['qid'],uid=request.session['uid']).count() != 0:
        q.qstore=1
    else:
        q.qstore=0


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
    discuss_hot=Discuss.objects.filter(support__gt=10,qid=request.session['qid']).order_by('-support')[0:10]

    # 100题以后增加一个随机验证码
    if (request.session['qid'] > 100) and (random.randint(1,50)==2) :
        request.session['next_verify']=2
    #不同的题型，出现相应不同的模板
    return render_to_response('baseQuestion.html', {'q' : q,\
            'includeQuestion':'question%d.html'%(q.qtype),'user':request.session,\
            'discuss_new':discuss_new,'discuss_hot':discuss_hot})

#带验证功能的下一题
def next_verify(request):
    if 'next_verify' in request.session and request.session['next_verify'] ==2:
        del(request.session['next_verify'])
        print 'success1'
        #验证成功，进入下一题
        return next(request)
    else:
        u=User.objects.get(id=request.session['uid'])
        u.forbidden=1
        u.save()
        import user as userview
        return userview.logout(request)


#下一题 
def next(request):

    #游客只能浏览前50题
    if request.session['uid'] ==0 and request.session['qid'] >=50:
        return HR(u'亲，请先登录，游客只能浏览前50题！')

    #邮箱未认证用户只能浏览前500题
    if request.session['degree'] <=1 and request.session['qid'] >=500:
        return HR(u'亲，请先完成邮箱认证，邮箱未认证用户只能浏览前500题！')

    # 2级用户只能浏览前2000题
    if request.session['degree'] <=2 and request.session['qid'] >=2000:
        return HR(u'亲，目前2级用户只能浏览前2000题！')

    #验证是否有爬虫
    if 'next_verify' in request.session and request.session['next_verify']==2:
        del(request.session['next_verify'])
        u=User.objects.get(id=request.session['uid'])
        u.forbidden=1
        u.save()
        import user as userview
        userview.logout(request)
        return HR(u'亲，不要爬我的小站了！')

    #如果存在用户登录 degree > 0 ，即非游客
    if request.session['degree']:
        user= User.objects.filter(id=request.session['uid'])[0]

        #自增下一题
        user.qid += 1
        #同步session
        request.session['qid'] = user.qid
        user.save()
    else:
        #如果为游客状态 session['qid'] 自增1
        request.session['qid'] += 1
    return HttpResponseRedirect('/showQuestion')



def pre(request):

    #如果存在用户登录 degree > 0 ，即非游客
    if request.session['degree']:
        user= User.objects.filter(id=request.session['uid'])[0]

        #自减上一题
        if user.qid > 1:
            user.qid -= 1
            #同步session
            request.session['qid'] = user.qid
            user.save()
    else:
        #如果为游客状态 session['qid'] 自减1
        if request.session['qid'] > 1:
            request.session['qid'] -= 1
    return HttpResponseRedirect('/showQuestion')


#跳转到指定题
def jump(request,qid):
    if request.session['degree'] < 2:
        return HR(u'对不起，您的权限不够！')

    q=Question.objects.filter(id=qid)
    if not q:
        return HR('没有此数据')

    user= User.objects.filter(id=request.session['uid'])[0]
    user.qid = qid
    request.session['qid'] = user.qid
    user.save()
 
    return HttpResponseRedirect('/showQuestion')
    

#收藏指定题
def store(request,qid):
    #未邮箱认证用户不能收藏
    if request.session['degree'] < 2:
        return

    qid=int(qid)
    s=Qstore.objects.filter(uid=request.session['uid'],question_id=abs(qid))
    if qid > 0 and (not s):
        qs=Qstore(uid=request.session['uid'],question_id=abs(qid))
        qs.save()
    #负的题号代表取消收藏
    elif qid < 0 and s:
        s[0].delete()
    else:
        return HR('wrong')
    return HR('success')
    


#编辑此题
def edit(request,qid):
    #如果权限不够不执行
    if request.session['degree'] < 4:
        return

    q=Question.objects.get(id=qid)
    #如果GET则显示question_edit页面
    if request.method == 'GET':
        user=request.session
        return render_to_response('question_edit_form.html',{'q':q,'user':user})

    #剩下的情况一般就只能是POST了，所以不要else了
    p=request.POST
    q.content=p['content']
    q.question=p['question']
    q.a=p['A']
    q.b=p['B']
    q.c=p['C']
    q.d=p['D']
    q.e=p['E']
    q.qexplain=p['explain']
    q.save()
    return HttpResponseRedirect('/showQuestion')





     

 
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



