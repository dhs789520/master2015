#coding:utf-8
# 关于用户登录，注册，退出登录，信息增改的操作均在此发生
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
def login(request):
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

        if user[0].forbidden != 0:
            return HR(u'对不起，用户被禁止,请返回重新登录')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    
         #设置session
        request.session['username']=user[0].username
        request.session['score']=user[0].score
        request.session['degree']=user[0].degree
        request.session['uid']=user[0].id
        request.session['qid']=user[0].qid
        return render_to_response('login_success.html')


#退出登录
def logout(request):
     #设置session
    request.session['username']='游客'
    request.session['score']=0
    request.session['degree']=0
    request.session['qid']=1
    request.session['uid']=0
    request.session['forbidden']=0
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



#用户注册
def reg(request):
     #如果GET则显示reg_from页面
    if request.method == 'GET':
        return render_to_response('reg_form.html')
     #如果POST数据，则处理数据
    elif request.method =='POST':
        username=request.POST['username']
        password=request.POST['password'] 
        password2=request.POST['password2']
        email=request.POST['email']
        verify=request.POST['verify']

        error=[]
         #如果用户名长度不正确
        if not 6<=len(username)<=12:
            error.append(u'用户名长度应在6到12之间')
        if not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9_]{4,15}$',username):
            error.append(u'用户名不规范，应以字符或数字开头，只能由字符，数字和下划线组成')

         #如果用户名已经存在
        if User.objects.filter(username=username).count() != 0:
            error.append(u'用户名已经存在')
         #如果密码长度不正确
        if not 6<=len(password)<=12:
            error.append(u'密码长度应在6到12之间')
         #如果两次密码输入不相同
        if password!=password2:
            error.append(u'两次输入密码不相同')
         #如果验证码错误
        if request.session['verify_code'].lower() != verify.lower():
            error.append(u'验证码输入错误')
         #如果email格式错误
        if not re.match(r'\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*',email):
            error.append(u'email格式错误')
         #email已经存在
        if User.objects.filter(email=email).count() != 0:
            error.append(u'email已经存在')

         #输入出错，返回注册页面，提示出错信息
        if error:
            reginfo={'username':username,'password':password,\
                    'email':email}
            return render_to_response('reg_form.html',{'error':error,'reginfo':reginfo})

        #生成email_verify_code用于邮箱有效性认证
        from uuid import uuid1
        email_verify_code=str(int(uuid1()))

        user=User(username=username,\
                password=password,\
                email=email,\
                email_verify_code=email_verify_code,\
                )
        user.save()

        #发送 email 认证  Email认证后，用户的degree 增加 1 ，也就可以发讨论信息了
        from django.core.mail import send_mail
        email_verify_url=r'http://m2015.sinaapp.com/email_verify/%s/%s'%(username,email_verify_code)
        emailmsg=u'尊敬的朋友，如果您在主治医师研讨班注册了帐号，请点击以下网址完成邮箱认证\n %s  \n如果没有注册，请忽略此邮件，谢谢！'%(email_verify_url)
        send_mail(u'用户邮箱认证',emailmsg,'dhs789520@163.com',[email],fail_silently=False)   


        #注册成功,设置session
        user= User.objects.filter(username=username)[0]
        request.session['user']=username
        request.session['uid']=user.id
        request.session['qid']=1
        request.session['score']=0 #新用户的操作积分为1
        request.session['degree']=1 #新用户的等级为1
        
        return render_to_response('reg_success.html',{'user':request.session})


#发送邮件以验证邮箱
def send_verify_email(request):
    if request.session['uid']== 0:
        return 
    user= User.objects.get(id=request.session['uid'])
    email_verify_code=user.email_verify_code
    if email_verify_code == 'success':
        return
    username=user.username
    email=user.email
    #发送 email 认证  Email认证后，用户的degree 增加 1 ，也就可以发讨论信息了
    from django.core.mail import send_mail
    email_verify_url=r'http://m2015.sinaapp.com/email_verify/%s/%s'%(username,email_verify_code)
    emailmsg=u'尊敬的朋友，如果您在主治医师研讨班注册了帐号，请点击以下网址完成邮箱认证\n %s  \n如果没有注册，请忽略此邮件，谢谢！'%(email_verify_url)
    send_mail(u'用户邮箱认证',emailmsg,'dhs789520@163.com',[email],fail_silently=False)   


    



#用户Email邮箱验证
def email_verify(request,username,email_verify_code):
    #删除末尾的空格，只保留字符
    email_verify_code=re.match(r'(\w+)',email_verify_code).group(0)

    if User.objects.filter(username=username,email_verify_code='success').count() ==1:
        return HR(u'您已经邮箱认证成功，请忽反复认证！')

    user=User.objects.filter(username=username,email_verify_code=email_verify_code)
    if user.count() == 1:
        u=user[0]
        u.email_verify_code='success'
        u.degree += 1
        request.session['degree']=u.degree
        u.save()
        return HR(u'认证成功')
    else:
        return HR(u'认证失败,请重新注册')
    


#用户信息显示页
def info(request):
     #如果用户首次进入网页
    if request.session['uid']== 0:
        user=request.session
    else:
        user=User.objects.get(id=request.session['uid'])


    #不同的题型，出现相应不同的模板
    return render_to_response('user_info.html', {'user':user} )


















