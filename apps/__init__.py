from flask import Flask
from config import config as cf
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mysqldb import MySQL
from apps.main.views import search
from apps.auth.views import auth

app = Flask(__name__)
app.secret_key = 'xiaoer'
app.config.from_object(cf['development'])
Bootstrap(app)
LoginManager(app)
MySQL(app)
app.register_blueprint(search)
app.register_blueprint(auth, url_prefix='/auth')


