import os
from flask_migrate import Migrate
from telecom_tianwang.app import create_app, db
from telecom_tianwang.app.models import User, Role

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)




@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

#app.run()
app.run(host='172.22.183.16',port=8081,debug=True)
#app.run(host='192.168.8.129',port=8083,debug=True)