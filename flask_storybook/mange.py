import os
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
from flask.ext.script import Manager

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:6Monthdleo@127.0.0.1/leodb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)


# class Role(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#     users = db.relationship('User', backref='role', lazy='dynamic')
#
#     def __repr__(self):
#         return '<Role %r>' % self.name
#
#
# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), unique=True, index=True)
#     role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
#
#     def __repr__(self):
#         return '<User %r>' % self.username

class Manhua(db.Model):
    __tablename__ = 'mhname'
    id = db.Column(db.VARCHAR(36), primary_key=True)
    mhname = db.Column(db.String(64), unique=True)
    pic_url = db.Column(db.String(128), unique=True)
    creat_time = db.Column(db.DATETIME)
    updata_time = db.Column(db.DATETIME)
    pic_base64data = db.Column(db.Text())
    last_updata = db.Column(db.DATETIME)
    last_updata_chaptername = db.Column(db.String(64), unique=True)

    #users = db.relationship('User', backref='role', lazy='dynamic')
    def __repr__(self):
        return '<Manhua %r>' % self.mhname

class Chapter(db.Model):
    __tablename__ = 'mhchapter'
    id = db.Column(db.VARCHAR(36), primary_key=True)
    mhname_id = db.Column(db.VARCHAR(36), db.ForeignKey('mhname.id'))
    data = db.Column(db.Text())
    chapter_nums = db.Column(db.Integer)
    pics_nums = db.Column(db.Integer)
    chapter_name = db.Column(db.String(64))
    creat_time = db.Column(db.DATETIME)
    updata_time = db.Column(db.DATETIME)

    db.UniqueConstraint(mhname_id,chapter_name)
    #users = db.relationship('User', backref='role', lazy='dynamic')
    def __repr__(self):
        return '<mhchapter %r>' % self.chapter_name

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


db.create_all()
db.session.commit()
# if __name__ == "__main__":
#     manager.run()