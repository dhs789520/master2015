#coding:utf-8
from django.contrib import admin
from models import Question,User,Record,Discuss,Vote


admin.site.register(Question)
admin.site.register(User)
admin.site.register(Record)
admin.site.register(Discuss)
admin.site.register(Vote)
