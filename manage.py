from flask_script import Manager, Shell

from apps import create_app, db
from apps.models import User

app = create_app('development')
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, user=User)

manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()

