#coding:utf-8
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


import views


#导入相关视图操作模块
from view import user
from view import question
from view import discuss

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'doctor.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    


    url(r'^$', views.index),
    url(r'^about$', views.about), #生成验证码图片页面
    url(r'^help$', views.help), #生成验证码图片页面
    url(r'^verify.jpg$', views.verifyimg), #生成验证码图片页面
    url(r'^cron$', views.cron),

    #相关操作存放于view.question
    url(r'^showQuestion', question.showQuestion),
    url(r'^showAnswer/(.+)', question.showAnswer),
    url(r'^next$', question.next),
    url(r'^next_verify$', question.next_verify),
    url(r'^pre$', question.pre),
    url(r'^jump$', question.jump),
    url(r'^search$', question.search),
    #url(r'^showQuestion/(\d+)$', views.showQuestion),


    #相关操作存放于view.discuss
    url(r'^vote', discuss.vote), #讨论投票
    url(r'^discuss$', discuss.discuss),#提交讨论
    
    #相关操作存放于view.user
    url(r'^reg$', user.reg),#用户注册页面
    url(r'^user_info$', user.info),#用户注册页面
    url(r'^send_verify_email$', user.send_verify_email),#发送邮箱验证邮件
    url(r'^email_verify/(.+)/(.+)$', user.email_verify),#邮箱验证页面
    url(r'^login$', user.login),#用户登录页面
    url(r'^logout$', user.logout),#退出登录页面

)
