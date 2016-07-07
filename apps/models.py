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
