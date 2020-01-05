from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # configure_uploads(app, photos)
    # patch_request_class(app)  # set maximum file size, default is 16MB
    from .novel import novel  as novel_blueprint
    app.register_blueprint(novel_blueprint, url_prefix='/novel')
    return app

