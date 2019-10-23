import datetime
endtime = datetime.datetime.now()
with open("log.txt","a+") as f:
    f.writelines(endtime.strftime( '%Y-%m-%d %H:%M:%S\n' ))