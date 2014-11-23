#coding:utf-8
# 用户讨论相关操作
import re
import random

from django.http.response import HttpResponse as HR
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.db.models import Q
#from django.template import RequestContext

from doctor.models import Question,User,Record,Discuss,Vote



#生成验证码函数
def verifyimg(request):
    from verify import genImg
    imgbuf,verify_code=genImg()
    request.session['verify_code']=verify_code
    return HR(imgbuf.getvalue(),'image/gif')



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


#讨论
def discuss(request):
    if request.session['degree'] <= 1:
        return HR(u'对不起，用户权限不购，不能参加讨论.')

    content=request.POST['content']
    purec=len(re.sub(r"<[^>]*?>",'',content)) #删除html标签
    c=len(re.findall(r'(<[^>]*?>)',content))+purec

    if c <10 or c >1000:
        return HR(u'对不起，讨论内容违规，字数应在10到1000之间')

    discuss=Discuss()
    discuss.content=content
    discuss.user_id=request.session['uid']
    discuss.qid=request.session['qid']
    discuss.save()
    return HttpResponseRedirect('/showQuestion')



