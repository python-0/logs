import os
from flask import request, render_template, Blueprint, current_app
from apps.utils import DatePicker
from apps.tasks import get_logs
from apps.models import Tasks, Hosts, Projects
from apps import db
from apps.main.forms import HostForm

cur_dir = os.path.abspath(os.path.dirname(__file__))
main = Blueprint('main', __name__)


@main.route('/index', methods=['GET'])
def index():
    if request.method == 'GET':
        projects = current_app.config['APPS_LOGS']
        form = DatePicker()
        return render_template('search.html', projects=projects, form=form)


@main.route('/hosts', methods=['GET', 'POST'])
def hosts():
    form = HostForm()
    if form.validate_on_submit():
        hostname = request.form['hostname']
        ipaddress = request.form['ipaddress']
        az = request.form['az']
        host = Hosts(hostname, ipaddress, az)
        db.session.add(host)
        db.session.commit()

    hosts = Hosts.query.order_by(db.asc(Hosts.id)).all()
    return render_template('main/hosts.html', hosts=hosts)




@main.route('/dl', methods=['POST'])
def dl():
    if request.method == 'POST':
        post = request.get_json()
        start_date = post['startTime'].encode('utf-8')
        end_date = post['endTime'].encode('utf-8')
        project = post['project'].encode('utf-8')
        host_name = post['hostName'].encode('utf-8')
        log_path = post['log_path'].encode('utf-8')
        user_name = 'admin'
        get_logs.delay(project, host_name, log_path, start_date, end_date, user_name)

        return ''
