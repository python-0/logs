from apps import create_app, db
from apps.models import User

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask_login import login_required


app = create_app('development')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, user=User)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


@app.route('/secret')
@login_required
def secret():
    return "only authenticated users are allowed"

if __name__ == '__main__':
    manager.run()

