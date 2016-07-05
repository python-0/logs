from flask import current_app, Blueprint, request, render_template,\
    redirect, url_for, flash
from apps.auth.forms import LoginForm
from apps import MySQL

auth = Blueprint('auth', __name__)
mysql = MySQL()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('auth/login.html', form=form)
    elif request.method == 'POST':
        cur = mysql.connection.cursor()
        username = request.form['username']
        password = request.form['password']
        cur.execute("""select count(*) from users where user_name="{}" and user_password="{}" """
                    .format(username, password)
                    )
        rv = cur.fetchone()[0]
        if rv == 0:
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('search.index'))

    return "wait..."


@auth.route('/apply', methods=['GET', 'POST'])
def apply():
    pass
