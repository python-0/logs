from flask import Flask
from config import config as cf
from flask_bootstrap import Bootstrap
from apps.cut_logs.views import search
app = Flask(__name__)
app.secret_key = 'xiaoer'
app.config.from_object(cf['development'])
Bootstrap(app)
app.register_blueprint(search)