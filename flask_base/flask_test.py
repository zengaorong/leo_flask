import os
from app import create_app
import platform
app = create_app(os.getenv('FLASK_CONFIG') or 'default')



sysstr = platform.system()
if(sysstr =="Windows"):
    app.run(host='127.0.0.1',port=8085,debug=True)
if(sysstr == "Linux"):
    app.run(host='127.0.0.1',port=8085,debug=True)