#!/bin/python
# coding=utf-8
#__author__ = 'CY'

'''迁移前请先清空新数据的表数据
    >SET FOREIGN_KEY_CHECKS=0;
    >TRUNCATE  hosts;
    >TRUNCATE  users;
    >TRUNCATE  pros;
    >TRUNCATE  dbs;
    >TRUNCATE  user_pro;
    >TRUNCATE  user_db;
    '''

import MySQLdb

def old_db(sql):
    conn = MySQLdb.connect(host='10.139.49.166',port=3306,user='opsmanager',passwd='opsmanager_rd',db='opsmanager',charset='utf8')
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

def new_db(sqli,data):
    conn_new = MySQLdb.connect(host='127.0.0.1',port=3306,user='opsmanager',passwd='opsmanager_rd',db='opsmanager',charset='utf8')
    cur_new = conn_new.cursor()
    cur_new.executemany(sqli,data)
    conn_new.commit()
    cur_new.close()
    conn_new.close()

# hosts表数据迁移
#hosts = old_db("select * from hosts")
#sqli="insert into hosts values(%s,%s,%s,%s,%s,%s)"
#new_db(sqli,hosts)

#users表数据迁移
#users = old_db("select id,username,name,password_hash,useremail,role,status,createtime from users")
#sql_users = "insert into users values(%s,%s,%s,%s,%s,%s,%s,%s)"
#new_db(sql_users,users)

#pros表迁移
#pros = old_db("select id,proname,prodomain,protype,propath,tomcatpath,svnurl,svnuser,svnpass,svnver,svnoldver,host_ip from pros")
#sql_pros = "insert into pros VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
#new_db(sql_pros,pros)

#user_pro表迁移
#user_pro = old_db("select * from user_pro")
#sql_user_pro = "insert into user_pro values (%s,%s)"
#new_db(sql_user_pro,user_pro)