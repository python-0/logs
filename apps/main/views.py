import subprocess
import os
from flask import request, render_template, Blueprint, current_app
from apps.main.utils import get_unix_time, DatePicker

cur_dir = os.path.abspath(os.path.dirname(__file__))
search = Blueprint('search', __name__)


@search.route('/search', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        projects = current_app.config['APPS_LOGS']
        form = DatePicker()
        return render_template('search.html', projects=projects, form=form)
    elif request.method == 'POST':
        start_date = request.form['start_date'].strip()
        end_date = request.form['end_date'].strip()
        app_name = request.form['app_name'].strip()
        app_logs = current_app.config[app_name]
        for host, log_path in app_logs.items():
            subprocess.call('/usr/local/bin/fab -f {}/get_logs.py -H {} \
				get_log:start_date={},end_date={},temp_file={},apps_log_path={}' \
                            .format(cur_dir, host, start_date,
                                    end_date,
                                    app_name + get_unix_time() + ".log",
                                    log_path), shell=True)

    return 'please wait ...'


@search.route('/dl', methods=['POST', 'GET'])
def dl():
    if request.method == 'POST':
        data = request.get_json(force=True)
        return ''
