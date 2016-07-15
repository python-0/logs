from flask import Flask
from config import config as cf, BaseConfig
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from celery import Celery


bootstrap = Bootstrap()
loginManager = LoginManager()
loginManager.session_protection = 'strong'
loginManager.login_view = 'auth.login'
mail = Mail()
db = SQLAlchemy()
celery = Celery(__name__, broker=BaseConfig.CELERY_BROKER_URL, include=['apps.tasks'])


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(cf[config_name])
    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    loginManager.init_app(app)
    celery.conf.update(app.config)
    cf[config_name].init(app)

    from apps.main.views import main
    app.register_blueprint(main)

    from apps.admin.views import admin
    app.register_blueprint(admin, url_prefix='/admin')

    from apps.auth.views import auth
    app.register_blueprint(auth, url_prefix='/auth')

    return app

