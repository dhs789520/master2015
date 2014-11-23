#coding:utf-8

#初始化数据
    #测试send mail
    from django.core.mail import send_mail
    send_mail('subject','message','dhs789520@qq.com',['65117032@qq.com'],fail_silently=False)

