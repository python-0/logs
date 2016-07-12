from flask import Blueprint, request, render_template,\
    redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from apps.auth.forms import LoginForm
from apps.models import User, Projects, Tasks
from apps import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user is not None and user.verify_password(password):
            login_user(user)
            return redirect(url_for('search.index'))
        flash('Invalid username or password', 'error')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You log out', 'info')
    return redirect(url_for('auth.login'))


@auth.route('/apply', methods=['GET', 'POST'])
def apply():
    pass
