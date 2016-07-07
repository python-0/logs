from flask import Flask
from config import config as cf
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail


bootstrap = Bootstrap()
loginManager = LoginManager()
loginManager.session_protection = 'strong'
loginManager.login_view = 'auth.login'
mail = Mail()
db = SQLAlchemy()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(cf[config])
    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    loginManager.init_app(app)

    from apps.main.views import search
    from apps.auth.views import auth
    app.register_blueprint(search)
    app.register_blueprint(auth, url_prefix='/auth')

    return app
