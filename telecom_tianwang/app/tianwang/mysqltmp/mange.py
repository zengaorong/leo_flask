#coding=utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:6Monthdleo@127.0.0.1/leodb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Watcher(db.Model):
    __tablename__ = 'watcher'
    id = db.Column(db.VARCHAR(36), primary_key=True)
    watchernum = db.Column(db.VARCHAR(5))
    watchername = db.Column(db.String(64))
    watchertown = db.Column(db.String(5))
    watchertype = db.Column(db.String(5))
    watcherserverip = db.Column(db.String(64))
    watcherip = db.Column(db.String(64))
    watcherlongitude = db.Column(db.DECIMAL(10,6))
    watcherlatitude = db.Column(db.DECIMAL(10,6))
    account = db.Column(db.VARCHAR(36))
    password = db.Column(db.VARCHAR(36))
    def __repr__(self):
        return '<Watcher %r>' % self.watchername

class Wterror(db.Model):
    __tablename__ = 'wterror'
    id = db.Column(db.VARCHAR(36), primary_key=True)
    watcher_id = db.Column(db.VARCHAR(36),db.ForeignKey('watcher.id'))
    creat_time = db.Column(db.DATETIME)
    updata_time = db.Column(db.DATETIME)
    work_for = db.Column(db.String(1024))
    erro_type = db.Column(db.VARCHAR(5))
    log_type = db.Column(db.VARCHAR(1))
    del_type = db.Column(db.VARCHAR(1))
    def __repr__(self):
        return '<Watcher %r>' % self.watchername

class Wtdel(db.Model):
    __tablename__ = 'wtdel'
    id = db.Column(db.VARCHAR(36), primary_key=True)
    watcher_id = db.Column(db.VARCHAR(36),db.ForeignKey('watcher.id'))
    creat_time = db.Column(db.DATETIME)
    updata_time = db.Column(db.DATETIME)
    work_for = db.Column(db.String(1024))
    erro_type = db.Column(db.VARCHAR(5))
    log_type = db.Column(db.VARCHAR(1))
    del_type = db.Column(db.VARCHAR(1))
    def __repr__(self):
        return '<Watcher %r>' % self.watchername

#  维护清单 物资使用情况表 材料类别（光分插片 服务器 光猫 球机 电缆） （更换） 该表对应故障表 使用故障条目的时间  修复描述 说明
#  目前 tpye = 1 光猫 2 服务器 3 球机 4 电表 5 缆 6 其他物品
class Maintenance(db.Model):
    __tablename__ = 'Mainten'
    id = db.Column(db.VARCHAR(36), primary_key=True)
    wterror_id = db.Column(db.VARCHAR(36),db.ForeignKey('wterror.id'))
    updata_time = db.Column(db.DATETIME)
    work_for = db.Column(db.String(1024))
    mainten_type = db.Column(db.VARCHAR(5))
    describe = db.Column(db.String(255))
    del_type = db.Column(db.VARCHAR(1))
    def __repr__(self):
        return '<Mainten %r>' % self.Mainten

#  记录公安球机清洗 故障等杂乱要求
#  id 创建时间 完成时间 内容 完成情况
class Policefor(db.Model):
    __tablename__ = 'policefor'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    creat_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    work_for = db.Column(db.String(1024))
    over_for = db.Column(db.String(1024))
    del_type = db.Column(db.VARCHAR(1))
    def __repr__(self):
        return '<policefor %r>' % self.id

#  天网ip使用情况记录
#  id 创建时间 ip ip使用地点描述 点位类型（球机 服务器 平台）
class Ipdetails(db.Model):
    __tablename__ = 'ipdetails'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    creat_time = db.Column(db.DATETIME)
    ip_str = db.Column(db.String(255))
    ip_position = db.Column(db.String(255))
    ip_type = db.Column(db.String(64))
    del_type = db.Column(db.VARCHAR(1))
    def __repr__(self):
        return '<ipdetails %r>' % self.id

#  天网杂乱消息记录
#  id 创建时间 ip ip使用地点描述 点位类型（球机 服务器 平台）
class Infordetails(db.Model):
    __tablename__ = 'infordetails'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    creat_time = db.Column(db.DATETIME)
    information = db.Column(db.Text())
    def __repr__(self):
        return '<infordetails %r>' % self.id

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)

db.create_all()
db.session.commit()