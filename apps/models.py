from apps import loginManager, db
from flask_login import UserMixin
from datetime import datetime


@loginManager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column('user_id', db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True)
    name = db.Column(db.String(20), index=True)
    password_hash = db.Column(db.String(128))
    confirmd = db.Column(db.Boolean, default=False)
    registerd_on = db.Column(db.DateTime)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.registered_on = datetime.utcnow()

    def __repr__(self):
        return '<User %r>' % self.name
