#coding=utf-8
import sys
import uuid
from datetime import  datetime,timedelta
from flask import render_template,request,redirect,url_for,current_app,jsonify
import flask_excel
from . import tianwang
from ..models import Wterror,Watcher,Wtdel,Maintenance,Policefor,Ipdetails,Infordetails
from .. import db
from .forms import MaintenForm,PoliceforForm,select_list,IpFrom
from sqlalchemy import and_
from .mysqltmp.fastping import run_fastping
import configparser


# 天网故障点位显示
@tianwang.route('/list', methods=['GET'])
def list():
    page = request.args.get('page', 1, type=int)
    pagination = db.session.query(Wterror,Watcher.watchername,Watcher.id,Watcher.watcherserverip,Watcher.watcherip,Watcher.watchertown).outerjoin(Watcher,Watcher.id == Wterror.watcher_id ).filter(Wterror.del_type == 0 ).order_by(Wterror.creat_time.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items


    listsize = pagination.total

    def get_week_day(date):
        week_day_dict = {
            0 : '星期一',
            1 : '星期二',
            2 : '星期三',
            3 : '星期四',
            4 : '星期五',
            5 : '星期六',
            6 : '星期天',
        }
        day = date.weekday()
        return week_day_dict[day]

    for key in posts:
        key.Wterror.week = get_week_day(key.Wterror.creat_time)
        key.Wterror.creat_time = key.Wterror.creat_time.strftime("%Y-%m-%d %H:%M:%S")
        wtdel = Wtdel.query.filter_by(watcher_id=key.id).order_by(Wtdel.updata_time.desc()).first()
        if wtdel!=None:
            key.Wterror.wtdeltime = wtdel.creat_time
        else:
            key.Wterror.wtdeltime = "暂无数据"

    # 获取最后更新时间
    with open("app/tianwang/mysqltmp/log.txt",'r') as f:
        time_list = f.readlines()
        print(time_list[-1])

    return render_template('tianwang/list.html',posts=posts,pagination=pagination,listsize=listsize,last_flush_time = time_list[-1].replace('\n',""))

# 天网故障点位显示
@tianwang.route('/list_to_excel', methods=['GET'])
def list_to_excel():

    # <th>序号</th>
    # <th>开始时间</th>
    # <th>开始星期</th>
    # <th>最近故障时间</th>

    page = request.args.get('page', 1, type=int)
    pagination = db.session.query(Wterror.updata_time,Wterror.creat_time,Wterror.work_for,Watcher.watchername,Watcher.id,Watcher.watcherserverip,Watcher.watcherip,Watcher.watchertown).outerjoin(Watcher,Watcher.id == Wterror.watcher_id ).filter(Wterror.del_type == 0 ).order_by(Wterror.creat_time.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items

    #
    # pagination = db.session.query(StoryChapter.chapter_id.label('章节'),Story.story_id.label('id'),Story.story_url.label('url')).outerjoin(Story,Story.story_id == StoryChapter.story_id ).filter(Story.story_id =='39651').paginate(
    #     1, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
    #     error_out=False)
    # column_names = ['章节','id', 'url']
    # story_list = pagination.items
    # return excel.make_response_from_query_sets(story_list, column_names, file_name='test',file_type='xlsx')



    listsize = pagination.total

    def get_week_day(date):
        week_day_dict = {
            0 : '星期一',
            1 : '星期二',
            2 : '星期三',
            3 : '星期四',
            4 : '星期五',
            5 : '星期六',
            6 : '星期天',
        }
        day = date.weekday()
        return week_day_dict[day]

    # for key in posts:
    #     # key.week = get_week_day(key.creat_time)
    #     print type(key)
    #     key.updata_time = key.updata_time.strftime("%Y-%m-%d %H:%M:%S")

    column_names = ['id','watchername','watchertown','updata_time', 'work_for','watcherserverip','watcherip']
    return flask_excel.make_response_from_query_sets(posts, column_names, file_name='test',file_type='xlsx')


# 删除日志
@tianwang.route('/delete',methods=['get'])
def delete():
    id = request.args.get('id', "", type=str)
    wterror = Wterror.query.filter_by(id=id).first()
    wterror.del_type = "1"
    dt = datetime.now()
    time = dt.strftime( '%Y-%m-%d %H:%M:%S' )
    wterror.updata_time = time

    wtdel = Wtdel(id=wterror.id,watcher_id=wterror.watcher_id,creat_time=wterror.creat_time,updata_time=wterror.updata_time,work_for=wterror.work_for,erro_type=wterror.erro_type,log_type=wterror.log_type,del_type=wterror.del_type)

    db.session.add(wtdel)
    db.session.commit()

    db.session.delete(wterror)
    db.session.commit()

    return redirect(url_for('tianwang.list'))

# 故障提交表单
@tianwang.route('/logbook_today',methods=['GET', 'POST'])
def logbook_today():
    id = request.args.get('id', "", type=str)
    wterror = Wterror.query.filter_by(id=id).first()
    watcher = Watcher.query.filter_by(id=wterror.watcher_id).first()
    return render_template('tianwang/twfrom.html',wterror=wterror,watcher=watcher)

# 故障保存
@tianwang.route('/savelog', methods=['POST'])
def savelog():
    id = request.form.get('id', "", type=str)
    work_for = request.form.get('work_for', "", type=str)
    if id != "":
        wterror = Wterror.query.filter_by(id=id).first()
        wterror.work_for = work_for

        db.session.add(wterror)
        db.session.commit()
        return redirect(url_for('tianwang.list'))
    return '''<h1>数据错误<h1> <a href="/tianwang/logbook_today?id=%s">返回</a>''' %(id)


# 今日恢复
@tianwang.route('/list_ys', methods=['GET'])
def list_ys():
    dt = datetime.today().strftime( '%Y-%m-%d' )
    dt = datetime.strptime(dt,'%Y-%m-%d')
    oneday = timedelta(days=1)
    yesterday = dt-oneday
    time = yesterday.strftime( '%Y-%m-%d %H:%M:%S' )
    print(time)

    # 获取当前时间
    now = datetime.now()
    # 获取今天零点
    zeroToday = now - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,microseconds=now.microsecond)
    # 获取23:59:59
    lastToday = zeroToday - timedelta(hours=23, minutes=59, seconds=59)
    # 获取前一天的当前时间
    yesterdayNow = now - timedelta(hours=23, minutes=59, seconds=59)
    # 获取明天的当前时间
    tomorrowNow = now + timedelta(hours=23, minutes=59, seconds=59)

    # Wtdel.creat_time >= zeroToday and Wtdel.creat_time<=now



    page = request.args.get('page', 1, type=int)

    pagination = db.session.query(Wtdel,Watcher.watchername,Watcher.id,Watcher.watcherserverip,Watcher.watcherip,Watcher.watchertown ).outerjoin(Watcher,Watcher.id == Wtdel.watcher_id).filter(and_(Wtdel.updata_time >= lastToday  , Wtdel.updata_time<zeroToday)).order_by(Wtdel.updata_time.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)

    print(db.session.query(Wtdel,Watcher.watchername,Watcher.id,Watcher.watcherserverip,Watcher.watcherip,Watcher.watchertown ).outerjoin(Watcher,Watcher.id == Wtdel.watcher_id).filter(and_(Wtdel.updata_time >= lastToday  , Wtdel.updata_time<zeroToday)).order_by(Wtdel.updata_time.desc()))

    # pagination = db.session.query(Wtdel).filter(and_(Wtdel.creat_time >= lastToday  , Wtdel.creat_time<now)).order_by(Wtdel.creat_time.desc()).paginate(
    #     page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
    #     error_out=False)
    posts = pagination.items

    listsize = pagination.total

    def get_week_day(date):
        week_day_dict = {
            0 : '星期一',
            1 : '星期二',
            2 : '星期三',
            3 : '星期四',
            4 : '星期五',
            5 : '星期六',
            6 : '星期天',
        }
        day = date.weekday()
        return week_day_dict[day]

    for key in posts:
        key.Wtdel.week = get_week_day(key.Wtdel.creat_time)
        key.Wtdel.creat_time = key.Wtdel.creat_time.strftime("%Y-%m-%d %H:%M:%S")


    return render_template('tianwang/rclist.html',posts=posts,pagination=pagination,listsize=listsize)


@tianwang.route('/list_td', methods=['GET'])
def list_td():
    dt = datetime.today().strftime( '%Y-%m-%d' )
    # 获取当前时间
    now = datetime.now()
    page = request.args.get('page', 1, type=int)
    pagination = db.session.query(Wtdel,Watcher.watchername,Watcher.id,Watcher.watcherserverip,Watcher.watcherip,Watcher.watchertown ).outerjoin(Watcher,Watcher.id == Wtdel.watcher_id).filter(and_(Wtdel.updata_time >= dt  , Wtdel.updata_time<now)).order_by(Wtdel.updata_time.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    listsize = pagination.total
    def get_week_day(date):
        week_day_dict = {
            0 : '星期一',
            1 : '星期二',
            2 : '星期三',
            3 : '星期四',
            4 : '星期五',
            5 : '星期六',
            6 : '星期天',
        }
        day = date.weekday()
        return week_day_dict[day]

    for key in posts:
        key.Wtdel.week = get_week_day(key.Wtdel.creat_time)
        key.Wtdel.creat_time = key.Wtdel.creat_time.strftime("%Y-%m-%d %H:%M:%S")


    return render_template('tianwang/tdlist.html',posts=posts,pagination=pagination,listsize=listsize)



@tianwang.route('/test',methods=['GET', 'POST'])
def test():
    return render_template('tianwang/test.html')


@tianwang.route('/register', methods=['GET', 'POST'])
def register():
    form = MaintenForm()
    if form.validate_on_submit():
        maintenance = Maintenance(work_for=form.work_for.data,
                           select_mainten_type=form.select_mainten_type.data,
                           describe=form.describe.data)
        db.session.add(maintenance)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('tianwang/register.html', form=form)

@tianwang.route('/reflush', methods=['GET', 'POST'])
def reflush():
    run_fastping("app/tianwang/mysqltmp/安福天网汇总.xls")
    return jsonify(result = "ok")

@tianwang.route('/flush_data', methods=['GET', 'POST'])
def flush_data():
    return render_template('tianwang/flush.html')

@tianwang.route('/policefor/<police_for>', methods=['GET', 'POST'])
def policefor(police_for):
    form = PoliceforForm()
    if form.validate_on_submit():
        now_time = datetime.now()
        policefor = Policefor(creat_time = now_time,
                              work_for=form.work_for.data,
                              over_for=form.over_for.data,)
        db.session.add(policefor)
        db.session.commit()
        return "add success"
    # form.over_for.data = "fjisaofjsio"
    # form.work_for.data = "fjisaofjsio"

    # id = request.args.get('id', "", type=str)
    # picsname = None
    # if(id!=""):
    #     manhua = Manhua.query.filter_by(id=id).first()
    #     if(manhua.pic_url!=""and manhua.pic_url!=None):
    #         picsname = manhua.pic_url.split('/')[-1]
    #     picsname = urllib.unquote(str(picsname))
    # else:
    #     manhua = Manhua(id=None,mhname="",pic_base64data="",)
    # return render_template('mhcontrol/backfrom.html',manhua=manhua,picsname=picsname)

    return render_template('tianwang/register.html', form=form)

@tianwang.route('/policelist', methods=['GET', 'POST'])
def policelist():
    dt = datetime.today().strftime( '%Y-%m-%d' )
    # 获取当前时间
    now = datetime.now()
    page = request.args.get('page', 1, type=int)
    pagination = db.session.query(Policefor).order_by(Policefor.creat_time.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    listsize = pagination.total
    return render_template('tianwang/policeforlist.html',posts=posts,pagination=pagination,listsize=listsize)


# # 故障提交表单
# @tianwang.route('/police_for',methods=['GET', 'POST'])
# def police_for():
#     id = request.args.get('id', "", type=str)
#     wterror = Wterror.query.filter_by(id=id).first()
#     watcher = Watcher.query.filter_by(id=wterror.watcher_id).first()
#     return render_template('tianwang/register.html',wterror=wterror,watcher=watcher)



# 天网信息记录
# 提供两个类型的检索 IP 和 名称  172.22.180.10  自己处理可用IP段  设置一个附录表格 可用富文本  比如联系人电话 号码  杂事等
@tianwang.route('/details', methods=['GET','POST'])
def details():
    # 检测是否带参数
    ip_str = request.form.get('qu_name', "", type=str)
    pagination_qu_name = request.args.get('qu_name', "", type=str)

    position_name = request.form.get('position_name', "", type=str)
    pagination_position_name = request.args.get('position_name', "", type=str)


    cf = configparser.ConfigParser()
    cf.read("app/tianwang/IPdetail.config")
    print(cf)
    cityIP = cf.get("IP", "cityIP")
    townIP = cf.get("IP", "townIP")

    print(pagination_position_name)
    # 存在搜索参数
    if ip_str!="" or pagination_qu_name!="" or position_name!="" or pagination_position_name!="":
        form = select_list()
        if ip_str!="":
            pagination_qu_name = ip_str
        if position_name!="":
            pagination_position_name = position_name

        form.qu_name.data = pagination_qu_name
        form.position_name.data = pagination_position_name
        page = request.args.get('page', 1, type=int)
        pagination = db.session.query(Ipdetails).filter(Ipdetails.del_type!=-1, Ipdetails.ip_str.like('%' + pagination_qu_name + '%'),Ipdetails.ip_position.like('%' + pagination_position_name + '%')).order_by(Ipdetails.ip_str.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
        posts = pagination.items
        listsize = pagination.total

        return render_template('tianwang/details.html',posts=posts,pagination=pagination,listsize=listsize,form=form,qu_name=pagination_qu_name,position_name=pagination_position_name,cityIP=cityIP,townIP=townIP)


    page = request.args.get('page', 1, type=int)
    pagination = db.session.query(Ipdetails).filter(Ipdetails.del_type!=-1).order_by(Ipdetails.ip_str.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    listsize = pagination.total

    form = select_list()
    return render_template('tianwang/details.html',posts=posts,pagination=pagination,listsize=listsize,form=form,cityIP=cityIP,townIP=townIP)


@tianwang.route('/editip', methods=['GET', 'POST'])
def editip():
    form = IpFrom()

    cf = configparser.ConfigParser()
    cf.read("app/tianwang/IPdetail.config")
    cityIP = cf.get("IP", "cityIP")
    townIP = cf.get("IP", "townIP")


    if form.validate_on_submit():
        cf.set("IP","cityIP",form.cityIP.data)
        cf.set("IP","townIP",form.townIP.data)

        with open("app/tianwang/IPdetail.config",'w') as fw:
            cf.write(fw)
            return redirect(url_for('tianwang.details'))

    form.cityIP.data = cityIP
    form.townIP.data = townIP
    return render_template('tianwang/register.html', form=form)