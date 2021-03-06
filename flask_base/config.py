import os
from ext import db
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    # MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.qq.com')
    # MAIL_PORT = int(os.environ.get('MAIL_PORT', '465'))
    # MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'true').lower() in \
    #     ['true', 'on', '1']
    # MAIL_USERNAME = 'zengaorong@qq.com'
    # MAIL_PASSWORD = 'xmghqcdjsckpebci'
    # FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    # FLASKY_MAIL_SENDER = 'zengaorong@qq.com'
    # FLASKY_ADMIN = '1904959670@qq.com'
    UPLOADED_PHOTOS_DEST = os.getcwd() + '/app/static/upload'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASKY_POSTS_PER_PAGE = 16
    FLASKY_POSTS_CHAP_PAGE = 100
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:7monthdleo@127.0.0.1:3306/mydb'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:6Monthdleo@127.0.0.1/leodb'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:6Monthdleo@127.0.0.1/leodb'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}





# #数据库配置信息
# HOSTNAME = '127.0.0.1'
# PORT     = '3306'
# DATABASE = 'mydb'
# USERNAME = 'root'
# PASSWORD = '7monthdleo'
# DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
#
# SQLALCHEMY_DATABASE_URI = DB_URI
# SQLALCHEMY_TRACK_MODIFICATIONS = False