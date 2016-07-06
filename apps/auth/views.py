from flask import Blueprint, request, render_template,\
    redirect, url_for, flash

from apps.auth.forms import LoginForm
from apps.models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('auth/login.html', form=form)
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user is None:
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('search.index'))

    return "wait..."


@auth.route('/apply', methods=['GET', 'POST'])
def apply():
    pass
