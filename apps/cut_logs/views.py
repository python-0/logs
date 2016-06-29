import subprocess
import os
from flask import send_from_directory, request, render_template, Blueprint, current_app
from apps.cut_logs.utils import get_unix_time
import config

cur_dir = os.path.abspath( os.path.dirname(__file__) )
search = Blueprint('search', __name__) 

@search.route('/search', methods=['POST', 'GET'])
def se():
	error = None
	if request.method == 'GET':
		return render_template('search.html')
	elif request.method == 'POST':
		start_date = request.form['start_date'].strip()
		end_date   = request.form['end_date'].strip()
		app_name   = request.form['app_name'].strip()
		print current_app.config
		app_logs   = current_app.config[app_name]
		for host,log_path in app_logs.items():
			subprocess.call('/usr/local/bin/fab -f {}/get_logs.py -H {} \
				get_log:start_date={},end_date={},temp_file={},apps_log_path={}'.format(cur_dir, host, start_date, end_date, app_name+get_unix_time()+".log", log_path), shell=True)

	return 'please wait ...'


@search.route("/dl")
def dl():
	return send_from_directory(app.config['logs_dir'], filename='abcd.txt', as_attachment=True)

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5000)
