from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand
from flask_login import login_required

from apps import create_app, db
from apps.models import User, Hosts, Projects, Tasks

from flask_admin import Admin
from apps.admin.views import UserAdminView, AdminView, HostsAdminView, ProjectsAdminView

app = create_app('development')
manager = Manager(app)
migrate = Migrate(app, db)
server = Server(host="0.0.0.0")

admin = Admin(app, index_view=AdminView())
admin.add_view(UserAdminView(User, db.session))
admin.add_view(HostsAdminView(Hosts, db.session))
admin.add_view(ProjectsAdminView(Projects, db.session))


def make_shell_context():
    return dict(app=app, db=db, user=User, project=Projects, tasks=Tasks)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)
manager.add_command('runserver', server)


@app.route('/secret')
@login_required
def secret():
    return "only authenticated users are allowed"


if __name__ == '__main__':
    manager.run()


