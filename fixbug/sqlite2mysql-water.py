#coding:utf-8

#将sqlite 中的数据导入 mysql版本
#采用硬编码的方式，先读取sqlte再写入mysql
#保质保量
#
try:
    import sae.const
    MYSQL_HOST=sae.const.MYSQL_HOST
    MYSQL_USER=sae.const.MYSQL_USER
    MYSQL_PASS=sae.const.MYSQL_PASS
    MYSQL_DB=sae.const.MYSQL_DB
    MYSQL_PORT=sae.const.MYSQL_PORT
except:
    MYSQL_HOST='127.0.0.1'
    MYSQL_USER='root'
    MYSQL_PASS=''
    MYSQL_DB='question'
    MYSQL_PORT=3306


import sys 
import MySQLdb

reload(sys) 
sys.setdefaultencoding('utf-8') 
class Query:

    def __init__ (self):
        self.connect()

    def __del__(self):
        self.db_exit()


    def connect (self):
        self.db=MySQLdb.connect(host=MYSQL_HOST,user=MYSQL_USER,passwd=MYSQL_PASS,db=MYSQL_DB,port=int(MYSQL_PORT))
        self.db.set_character_set('utf8')
        self.dbc=self.db.cursor()
        self.dbc.execute('SET NAMES utf8;')
        self.dbc.execute('SET character_set_connection=utf8;')




    #插入数据库
    def insert(self,sql,keys):
        self.dbc.execute(sql,keys)
        return

	
    def db_exit(self):
        self.dbc.close()
        self.db.close()

if __name__=='__main__':
    db=Query()

    import sqlite3
    db3=sqlite3.connect('question.db')
    cur=db3.cursor()

    n=0
    while(1):
        cur.execute('select * from question where id > %d limit 1;'%(n))
        result=cur.fetchone()
        if result:
            r=list(result)
            db.insert("insert into doctor_question(subject,type,serial,content,question,A,B,C,D,E,answer,`explain`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8],r[9],r[10],r[11],r[12]])
            n=r[0]
        else :
            break


    print 'success'




















