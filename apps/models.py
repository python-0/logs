from apps import loginManager, db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


@loginManager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column('user_id', db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    name = db.Column(db.String(20), index=True)
    password_hash = db.Column(db.String(128))
    confirmd = db.Column(db.Boolean, default=False)
    registerd_on = db.Column(db.DateTime)

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password
        self.registered_on = datetime.utcnow()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.name


class Hosts(db.Model):
    __tablename__ = 'hosts'
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(30), unique=True)
    ipaddress = db.Column(db.String(20), unique=True)
    az = db.Column(db.String(20))

    def __init__(self, hostname, ip, az):
        self.az = az
        self.ipaddress = ip
        self.hostname = hostname


class Projects(db.Model):
    __tablename__ = 'projects'
    id = db.Column('project_id', db.Integer, primary_key=True)
    project_name = db.Column(db.String(70), unique=True)
    log_path = db.Column(db.String(100))
    host = db.Column(db.Integer, db.ForeignKey(Hosts.id))

    def __init__(self, id, project_name, log_path, host):
        self.id = id
        self.project_name = project_name
        self.host = host
        self.log_path = log_path


class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = db.Column('task_id', db.Integer, primary_key=True)
    start_date = db.Column(db.String(64))
    end_date = db.Column(db.String(64))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'))
    project = db.relationship('Projects', backref=db.backref('tasks', lazy='dynamic'))
