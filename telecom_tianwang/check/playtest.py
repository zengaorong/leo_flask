#coding=utf-8

from flask import render_template, redirect, request, url_for, flash,jsonify,send_from_directory, \
    current_app
from flask_login import login_user, logout_user, login_required, \
    current_user
import sys
import urllib
import os

reload(sys)
sys.setdefaultencoding('utf-8')

cwd = os.getcwd()
path= cwd + '/app/static/pics'


str = u"\u5bb6\u5ead\u6559\u5e08/1\xa0\u4ece\u610f\u5927\u5229\u6765\u7684\u5bb6\u4f19/1\xa0\u4ece\u610f\u5927\u5229\u6765\u7684\u5bb6\u4f190.jpg"
print repr(str)
print repr(str.encode('GBK', 'ignore'))


#
# print repr("家庭教师")
# print repr("家庭教师".encode('utf-8'))
# print repr("家庭教师".encode('GBK'))

# dir = '/app/static/pics/'
# files = os.listdir(cwd + '/app/static/pics/')
# for key in files:
#     print key