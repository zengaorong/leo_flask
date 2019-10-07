#coding=utf-8
import sys
import requests
import os
import ConfigParser
reload(sys)
sys.setdefaultencoding='utf-8'



cf = ConfigParser.ConfigParser()
cf.read("omg.config")

url = cf.get("server_url", "url")
ir = requests.get(url)

def mkdir(path):
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False
mkdir("pics")
sz = open(r'pics/test.jpg', 'wb').write(ir.content)