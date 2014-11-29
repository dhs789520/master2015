#coding:utf-8
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Question(models.Model):
    subject = models.CharField(max_length=100, blank=True)
    qtype = models.IntegerField(db_column='type',blank=True, null=True)
    qserial = models.IntegerField(db_column='serial',blank=True, null=True)
    content = models.CharField(max_length=800, blank=True)
    question = models.CharField(max_length=500, blank=False)
    a = models.CharField(db_column='A', max_length=200, blank=False) # Field name made lowercase.
    b = models.CharField(db_column='B', max_length=200, blank=False) # Field name made lowercase.
    c = models.CharField(db_column='C', max_length=200, blank=False) # Field name made lowercase.
    d = models.CharField(db_column='D', max_length=200, blank=False) # Field name made lowercase.
    e = models.CharField(db_column='E', max_length=200, blank=False) # Field name made lowercase.
    answer = models.CharField(max_length=50, blank=True)
    qexplain = models.CharField(db_column='explain',max_length=800, blank=True)

    def __unicode__(self):
        return "%d - %s"%(self.id ,self.question)


 #用户表
class User(models.Model):
    username = models.CharField(max_length=20,unique=True, blank=False,null=False)
    password = models.CharField(max_length=30,blank=False,null=False) 
    email = models.EmailField(max_length=500,blank=False,null=False) #Email
    email_verify_code = models.CharField(max_length=40,blank=True,null=True) # Email有效性验证码
    realname = models.CharField(max_length=2, blank=True,null=True) #真实姓名
    sex = models.CharField(max_length=2, blank=True,null=True) #性别
    hospital = models.CharField(max_length=100, blank=True,null=True) #医院
    major = models.CharField(max_length=100, blank=True,null=True) #专业
    photo = models.CharField(max_length=100, blank=True,null=True)#存储的是图片地址
    regDate = models.DateTimeField(auto_now_add=True, blank=True,null=True) #注册时间
    score = models.IntegerField(default=1, blank=True,null=True) #新用户注册即为1分，email认证为2分
    degree = models.IntegerField(default=1, blank=True,null=True) #新用户注册即为1级
    qid = models.IntegerField(default=1, blank=True,null=True) #用户最后浏览题目id
    forbidden = models.IntegerField(default=0, blank=False,null=False) #用户是否被禁止

    def __unicode__(self):
        return "%d - %s"%(self.id ,self.username)


#题目收藏表
class Qstore(models.Model):
    uid = models.IntegerField(db_index=True,blank=False, null=False)#索引
    question=models.ForeignKey(Question)
 
#答题记录表
class Record(models.Model):
    uid = models.IntegerField(db_index=True,blank=False, null=False)
    qid = models.IntegerField(blank=False, null=False)
    result = models.BooleanField(blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True, blank=True,null=True)

    def __unicode__(self):
        return "%d - %s"%(self.id ,self.uid)

#讨论记录表
class Discuss(models.Model):
     #使用外键 表中的字段为 user_id
    user=models.ForeignKey(User)
    qid = models.IntegerField(blank=False, null=False)
    content = models.TextField(blank=False, null=False)
    support = models.IntegerField(default=0,blank=True, null=True)
    oppose = models.IntegerField(default=0,blank=True, null=True)
    date = models.DateTimeField(db_index=True,auto_now_add=True, blank=True,null=True)

    def __unicode__(self):
        return "%d - %s"%(self.id ,self.content)

#投票记录表
class Vote(models.Model):
     #使用外键 表中的字段为 user_id
    user=models.ForeignKey(User)
    discuss=models.ForeignKey(Discuss)
     #vote 代表用户的投票 1 为支持票   -1 为反对票
    vote = models.IntegerField(blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True, blank=True,null=True)

    def __unicode__(self):
        return "%d - %s"%(self.id ,self.user)


