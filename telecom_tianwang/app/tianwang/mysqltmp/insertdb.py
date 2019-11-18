#coding=utf-8
import sys
import MySQLdb
import os
import re
import uuid
import platform
from datetime import datetime
from leotool.readexcel import readexcel_todict

reload(sys)
sys.setdefaultencoding('utf-8')
dataname = "leodb"
host='127.0.0.1'



def updata_watch_todb(list):
    conn= MySQLdb.connect(
        host= host,
        port = 3306,
        user='root',
        passwd='6Monthdleo',
        db = dataname ,
        charset='utf8'
    )
    cur = conn.cursor()
    sqli =  "insert into watcher(id,watchernum,watchername,watchertown,watchertype,watcherserverip,watcherip,watcherlongitude,watcherlatitude,account,password)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cur.executemany(sqli,list)
    conn.commit()
    conn.close()

def updata_ip_todb(list):
    conn= MySQLdb.connect(
        host= host,
        port = 3306,
        user='root',
        passwd='6Monthdleo',
        db = dataname ,
        charset='utf8'
    )
    cur = conn.cursor()
    sqli =  "insert into ipdetails(creat_time,ip_str,ip_position,ip_type,del_type)values(%s,%s,%s,%s,%s)"
    cur.executemany(sqli,list)
    conn.commit()
    conn.close()

# 天网表信息插入
# tw_dict = readexcel_todict("安福天网汇总.xls".decode('utf-8'),1,1,0)
# temp_list = []
# for key in tw_dict:
#     print key
#     print tw_dict[key]
#     temp_list.append([tw_dict[key][1],str(tw_dict[key][0]),tw_dict[key][3],tw_dict[key][2],tw_dict[key][4],tw_dict[key][5],tw_dict[key][6],tw_dict[key][11],tw_dict[key][12],"admin","JADXtw2018"])

# ip 表信息插入
tw_dict = readexcel_todict("安福天网汇总.xls".decode('utf-8'),1,1,0)
temp_list = []
num = 0
for key in tw_dict:
    time = datetime.now()
    if tw_dict[key][5]!="":
        temp_list.append([time,tw_dict[key][5],tw_dict[key][3],tw_dict[key][4],0])
    if tw_dict[key][6]!="":
        temp_list.append([time,tw_dict[key][6],tw_dict[key][3],tw_dict[key][4],0])
    num+=1
    print num
updata_ip_todb(temp_list)



#updata_watch_todb(temp_list)