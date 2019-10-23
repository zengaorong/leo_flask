#coding=utf-8
from readexcel import readexcel_todict
import sys
import MySQLdb
import uuid
import subprocess
import xlwt
from datetime import  datetime,timedelta

reload(sys)
sys.setdefaultencoding('utf-8')
dataname = "leodb"
host='127.0.0.1'

# 查询每月修复的数据
def select_mouth_log_todb(time):
    conn= MySQLdb.connect(
        host= host,
        port = 3306,
        user='root',
        passwd='6Monthdleo',
        db = dataname ,
        charset='utf8'
    )

    # dt = datetime.today().strftime( '%Y-%m-%d' )
    # dt = datetime.strptime(dt,'%Y-%m-%d')
    # oneday = timedelta(days=1)
    # yesterday = dt-oneday
    # time = yesterday.strftime( '%Y-%m-%d %H:%M:%S' )
    # print time
    begintime = datetime.strptime(time,"%Y-%m")
    year = begintime.strftime("%Y")
    mouth = begintime.strftime("%m")
    if int(mouth) == 12:
        oneday = timedelta(days=1)
        endtime = begintime + oneday*31
    else:
        endtime = datetime.strptime(str(year) + '-' + str(int(mouth) + 1),"%Y-%m")

    cur = conn.cursor()
    print begintime,endtime
#     sql_select = '''
#     SELECT wtdel.id AS "wtdel_id", wtdel.watcher_id AS wtdel_watcher_id, wtdel.creat_time AS wtdel_creat_time, wtdel.updata_time AS wtdel_updata_time, wtdel.work_for AS wtdel_work_for, wtdel.erro_type AS wtdel_erro_type, wtdel.log_type AS wtdel_log_type, wtdel.del_type AS wtdel_del_type, watcher.watchername AS watcher_watchername, watcher.id AS watcher_id, watcher.watcherserverip AS watcher_watcherserverip, watcher.watcherip AS watcher_watcherip, watcher.watchertown AS watcher_watchertown
# FROM wtdel LEFT OUTER JOIN watcher ON watcher.id = wtdel.watcher_id
# WHERE wtdel.updata_time >= "%s" AND wtdel.updata_time < "%s" ORDER BY wtdel.updata_time DESC
#     '''%(begintime,endtime)
    sql_select = '''
    SELECT watcher.watchertown AS watcher_watchertown,wtdel.creat_time AS wtdel_creat_time, watcher.watchername AS watcher_watchername,wtdel.work_for AS wtdel_work_for,wtdel.updata_time AS wtdel_updata_time
FROM wtdel LEFT OUTER JOIN watcher ON watcher.id = wtdel.watcher_id 
WHERE wtdel.updata_time >= "%s" AND wtdel.updata_time < "%s" ORDER BY wtdel.updata_time asc
    '''%(begintime,endtime)
    select_have = cur.execute(sql_select)
    select_list = cur.fetchmany(select_have)

    fields = cur.description
    table_name = dataname
    workbook = xlwt.Workbook(encoding = 'utf-8')
    sheet = workbook.add_sheet('table_'+table_name,cell_overwrite_ok=True)

    # 字段替换 {'watcher_watchertown':'乡镇'，'wtdel_creat_time':'申告日期'，'watcher_watchername':'点位名称'}
    # 写上字段信息
    #fields_dict = {'watcher_watchertown':'乡镇','wtdel_creat_time':'申告日期','watcher_watchername':'点位名称'}
    # for field in range(0,len(fields)):
    #     if fields_dict.has_key(fields[field][0]):
    #         sheet.write(0,field,fields_dict[fields[field][0]])

    fields_list = ["序号","乡镇","申告日期","前端点名称","故障原因"]
    for field in range(0,len(fields_list)):
        sheet.write(0,field,fields_list[field])



    if select_list==None:
        return
    out_list = []
    # 去除秒短记录
    for key in select_list:
        oneday = timedelta(hours=2)
        if key[4] - key[1] > oneday :
            out_list.append(key)

    # 合并同日期记录
    # 11月1日	江下村至钦村路口/乡政府路口（变压器边）	不在线	吊死	修复
    td_time = None
    work_for_strs = ""
    watcher_name_strs = ""
    write_list = []
    num = 0

    for cell in out_list:
        print cell[4]
        now_time = cell[4].strftime("%Y-%m-%d")
        if td_time!=now_time:
            if td_time == None:
                td_time = now_time

                work_for_strs = work_for_strs + '/' + str(out_list[num][3])
                watcher_name_strs = watcher_name_strs + '/' + str(out_list[num][2])
            else:
                write_list.append([td_time,watcher_name_strs,work_for_strs])
                td_time = now_time
                work_for_strs = ""
                watcher_name_strs = ""
        else:
            work_for_strs = work_for_strs + '/' + str(out_list[num][3])
            watcher_name_strs = watcher_name_strs + '/' + str(out_list[num][2])

        num = num + 1

    write_list.append([td_time,watcher_name_strs,work_for_strs])

    # 获取并写入数据段信息
    row = 1
    col = 0
    for row in range(1,len(write_list)+1):
        sheet.write(row,0,u'%s'%row)
        sheet.write(row,1,u'%s'%write_list[row-1][0])
        sheet.write(row,2,u'%s'%write_list[row-1][1])
        sheet.write(row,3,u'%s'%write_list[row-1][2])


    workbook.save("output.xlsx")
    #
    # names = cur.execute(sql_str)
    # info = cur.fetchmany(names)
    # if info:
    #     temp_tuple = info[0]
    #     dt = datetime.now()
    #     time = dt.strftime( '%Y-%m-%d %H:%M:%S' )
    #     # (uuid.uuid1(),temp_tuple[0],time,time,"123456","0","0","0")
    #     sql_str = '''insert into wterror(id,watcher_id,creat_time,updata_time,work_for,erro_type,log_type,del_type)values("%s","%s","%s","%s","%s","%s","%s","%s")'''%(uuid.uuid1(),temp_tuple[0],time,time,error_for,"0","0","0")
    #     print sql_str
    #     names = cur.execute(sql_str)
    #     print names
    # conn.commit()
    # conn.close()
select_mouth_log_todb("2019-9")