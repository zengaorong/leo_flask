#coding=utf-8
import threading
import configparser
import time
import datetime
from flask_mode.app.tianwang.mysqltmp.readexcel import readexcel_todict
from flask_mode.app.tianwang.mysqltmp.opereat import updata_watch_todb,select_wterror,delete_wterror_todb,delete_check

import subprocess

def check_is_nums(str_check):
    isnum = True
    for key in str_check.decode('utf-8'):
        if u'\u0030'<=key<=u'\u0039':
            pass
        else:
            isnum = False
            return isnum

    if str_check == "":
        isnum = False
    return isnum


def __load_one_chapter(list,resoult_list,dic2):
    # list[5] list[6]  服务器IP  球机IP
    if(list[14]=="不考核"):
        return
    if(list[5]=="" or list[6]==""):
        ip = list[5]
        if(ip == ""):
            ip = list[6]

        ret = subprocess.call("ping  %s -w 2000" % ip,shell=True,stdout=subprocess.PIPE)
        if(ret==1):
            resoult_list.append([list[1],list[3],"单IP设备，设备异常",list[2],dic2[list[2]][0]])
        return

    ret_server = subprocess.call("ping  %s -w 2000" % list[5],shell=True,stdout=subprocess.PIPE)
    ret_work = subprocess.call("ping  %s -w 2000" % list[6],shell=True,stdout=subprocess.PIPE)

    # isrun = True
    # stop_num = 2
    # ret_server = 1
    # ret_work = 1
    # while isrun:
    #     try:
    #         ret_server = subprocess.call("ping  %s -w 2000" % list[5],shell=True,stdout=subprocess.PIPE)
    #         ret_work = subprocess.call("ping  %s -w 2000" % list[6],shell=True,stdout=subprocess.PIPE)
    #     except Exception,e:
    #         stop_num=stop_num-1
    #         if stop_num==0:
    #             isrun=False
    #             print e

    if ret_server == 0 and ret_work == 0:
       pass
    else:
        wrong_str = ""
        if ret_server == 1:
            wrong_str = "服务器不在线"
        if ret_work == 1:
            wrong_str = "设备不在线"
        if ret_server == 1 and ret_work == 1:
            wrong_str = "均不在线"

        #print dic2[list[2]][0]
        resoult_list.append([list[1],list[3],wrong_str,list[2],dic2[list[2]][0]])
    # if ret == 0:
    #     str = '%s is alive' % check_name
    #     resoult_list.append(str)
    # elif ret == 1:
    #     str = '%s : %s is not alive' % (check_name,check_ip)
    #     resoult_list.append(str)


# 下载项目名称 文件夹名称 文件数量 下载的URL 文件的类型
def down_data(dic1,dic2):
    # 存在问题的表： 点位编码 点位名称 故障原因 乡镇 区域
    resoult_list = []
    download_threads = []
    thread_nums = 20

    for i in dic1:
        # threadnums = 0
        # threadnums = threadnums + 1
        # print "ping:" +  ip_key[i][1]
        # if threadnums > 5:
        #     time.sleep(1 + threadnums-5)
        thread_alives = 0
        for searchs in download_threads:
            if searchs.isAlive():
                thread_alives = thread_alives + 1
        print(thread_alives)

        if thread_alives > thread_nums:
            print("time sleep")
            sleep = True
            while sleep:
                thread_alives = 0
                for serchs in download_threads:
                    if serchs.isAlive():
                        thread_alives = thread_alives + 1

                if thread_alives > 20:
                    time.sleep(0.1)
                else:
                    sleep = False
                    download_thread = threading.Thread(target=__load_one_chapter,args=(dic1[i],resoult_list,dic2))

        else:
            download_thread = threading.Thread(target=__load_one_chapter,args=(dic1[i],resoult_list,dic2))


        download_threads.append(download_thread)
        download_thread.start()
    [ t.join() for t in download_threads ]

    # print resoult_list[0]
    # for key in resoult_list[0]:
    #     print key
    # f = open("wrong",'w+')
    # wrong_str = ''
    # for key in resoult_list:
    #     wrong_str = wrong_str + key + '\n'
    #
    # f.writelines(wrong_str)
    # f.close()
    dict_for_out = {}
    for key in resoult_list:
        if key[4] in dict_for_out:
            dict_for_out[key[4]].append(key)
        else:
            dict_for_out[key[4]] = [key]

    temp_error_list = []
    for key in dict_for_out:
        for wrong_list in dict_for_out[key]:
            updata_watch_todb(wrong_list[0],wrong_list[2])
            temp_error_list.append(wrong_list[0])

    error_list = select_wterror()
    for key in error_list:
        print(key[1])
        if key[1] not in temp_error_list:
            if delete_check(key[1]):
                delete_wterror_todb(key[1])
    # f = open("out.txt",'w+')
    # wrong_str = ''
    # wrong_str_name = ''
    # end_str = ''
    # for key in dict_for_out:
    #     for wrong_list in dict_for_out[key]:
    #         wrong_str = wrong_str + wrong_list[4] + '\t' + wrong_list[3] + '\t' + wrong_list[0] + '\t' +  wrong_list[1] + '\t' +  wrong_list[2]      + '\n'
    #         if wrong_list[2]=="服务器不在线" or wrong_list[2]=="均不在线":
    #             end_str = end_str + wrong_list[0] + ','
    #             wrong_str_name = wrong_str_name + wrong_list[1] + '/'
    #
    # wrong_str = wrong_str + end_str + '\n'
    # wrong_str = wrong_str + wrong_str_name + '\n'
    # f.writelines(wrong_str)
    # f.close()

def run_fastping(file_url):
    # print "\xb0\xb2\xb8\xa3\xcc\xec\xcd\xf8\xbb\xe3\xd7\xdc.xls".decode('gbk')

    ret_server = subprocess.call("ping  %s -w 2000" % "172.22.180.1",shell=True,stdout=subprocess.PIPE)
    if ret_server == 1:
        pass
    else:
        dic1 = readexcel_todict("app/tianwang/mysqltmp/安福天网汇总.xls",1,1,0)
        dic2 = readexcel_todict("app/tianwang/mysqltmp/安福天网汇总.xls", 1, 1, 1)
        down_data(dic1,dic2)
        starttime = datetime.datetime.now()

        with open("app/tianwang/mysqltmp/log.txt","a+") as f:
            f.writelines(starttime.strftime( '%Y-%m-%d %H:%M:%S\n' ))


if __name__ == '__main__':
    dic2 = readexcel_todict("安福天网汇总.xls",1,1,1)
    dic1 = readexcel_todict("安福天网汇总.xls", 1, 1, 0)
    cf = configparser.ConfigParser()
    cf.read("seting.config")
    hour = cf.getint("time", "hour")
    secode = cf.getint("time", "secode")
    minutes = cf.getint("time", "minutes")
    times = hour*60*60 + secode*60 + minutes

    isrun = True
    starttime = datetime.datetime.now()
    num = 0
    while isrun:
        endtime = datetime.datetime.now()
        # print (endtime - starttime)
        if (endtime - starttime).seconds > times:
            print("rum" + str(num) + "time")
            print(endtime.strftime( '%Y-%m-%d %H:%M:%S' ))
            ret_server = subprocess.call("ping  %s -w 2000" % "172.22.180.1",shell=True,stdout=subprocess.PIPE)
            if ret_server == 1:
                pass
            else:
                down_data(dic1,dic2)

            starttime = datetime.datetime.now()

            with open("log.txt","a+") as f:
                f.writelines(endtime.strftime( '%Y-%m-%d %H:%M:%S\n' ))
        else:
            time.sleep(times/2)



