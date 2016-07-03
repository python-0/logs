from flask import current_app, Blueprint, request, render_template
from apps.auth.forms import LoginForm
from apps import MySQL

auth = Blueprint('auth', __name__)

mysql = MySQL()

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if request.method == 'GET':
		return render_template('auth/login.html', form = form)
	elif request.method == 'POST':
		cur = mysql.connection.cursor()
		cur.execute("""select * from users""")
		rv = cur.fetchall()
		print(rv)

@auth.route('/apply', methods=['GET', 'POST'])
def apply():
	pass