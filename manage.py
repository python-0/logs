from apps import create_app, manager, db
from apps.models import User

app = create_app('development')


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, user=User)

if __name__ == '__main__':
    manager.run()

