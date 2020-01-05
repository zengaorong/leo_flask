from flask_migrate import Migrate,MigrateCommand
from ext import db
from flask_script import Manager
from app import models,create_app


app = create_app('default')      #实例化一个app对象
manager = Manager(app)  #实例化一个manager对象
Migrate(app,db)    #绑定 数据库与app,建立关系
manager.add_command('db',MigrateCommand)    #添加迁移命令集 到脚本命令

#如果是以此脚本作为主脚本程序，就执行
if __name__ == '__main__':
    manager.run()