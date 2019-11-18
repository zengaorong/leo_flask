#coding=utf-8
import sys
from flask import Flask, render_template
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)



@app.route('/read', methods=['GET', 'POST'])
def jq():
    return render_template("b.html")

#app.run(host='127.0.0.1',port=8084,debug=True)




from datetime import datetime
dt = datetime.now()
print   '今天是这周的第%s天 '  % dt.strftime( '%w' )


# print dt
# # 将datatime类型的数据转换为字符串类型的数据，用%s插入到数据库中。
# s = str(dt)[:-7]
# print s

#print s print type(s) # 将字符串类型的数据从数据库读出来后，转换为datetime.datatime 类型的数据
# date = datetime.strptime(s,'%Y-%m-%d %H:%M:%S') print date print type(date)

