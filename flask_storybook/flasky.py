import os
from flask_migrate import Migrate
from flask_mode.app import create_app, db
from flask_mode.app.models import User, Role

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)






#app.run()
app.run(host='172.22.183.16', port=8081, debug=True)
#app.run(host='192.168.8.129',port=8083,debug=True)