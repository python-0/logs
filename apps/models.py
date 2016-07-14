from apps import loginManager, db
from flask_login import UserMixin
from datetime import datetime
import pytz
from werkzeug.security import generate_password_hash, check_password_hash


@loginManager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column('user_id', db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(60), index=True, unique=True)
    name = db.Column(db.String(20), index=True)
    password_hash = db.Column(db.String(128))
    confirmd = db.Column(db.Boolean, default=False)
    admin = db.Column(db.Boolean, default=False)
    registerd_on = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Chongqing')))

    def __init__(self, email, name, password, admin, confirmd):
        self.email = email
        self.name = name
        self.password = password
        self.admin = admin
        self.confirmd = confirmd

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def is_admin(self):
        return self.admin

    def is_confirmd(self):
        return self.confirmd

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.name


class Hosts(db.Model):
    __tablename__ = 'hosts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hostname = db.Column(db.String(30), unique=True)
    ipaddress = db.Column(db.String(20), unique=True)
    az = db.Column(db.String(20))

    def __init__(self, hostname, ip, az):
        self.az = az
        self.ipaddress = ip
        self.hostname = hostname

    def __str__(self):
        return self.hostname


class Projects(db.Model):
    __tablename__ = 'projects'
    id = db.Column('project_id', db.Integer, primary_key=True, autoincrement=True)
    project_name = db.Column(db.String(70), unique=True)
    log_path = db.Column(db.Unicode(128))
    host_id = db.Column(db.Integer, db.ForeignKey(Hosts.id))
    host = db.relationship('Hosts', backref=db.backref('projects', lazy='dynamic'))

    def __init__(self, id, project_name, log_path, host):
        self.id = id
        self.project_name = project_name
        self.host = host
        self.log_path = log_path

    def __str__(self):
        return self.project_name


class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = db.Column('task_id', db.Integer, primary_key=True, autoincrement=True)
    start_date = db.Column(db.String(64))
    end_date = db.Column(db.String(64))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'))
    project = db.relationship('Projects', backref=db.backref('tasks', lazy='dynamic'))


projects_hosts = db.Table(
    'projects_hosts',
    db.Column('host_id', db.Integer, db.ForeignKey('hosts.id')),
    db.Column('project_id', db.Integer, db.ForeignKey('projects.project_id'))
)
