import os
import sys
from fabric.api import task, run, get


def cut_log(start_date, end_date, temp_file, apps_log_path):
    search_str = "sed -n '/{}/,/{}/p' {} > /tmp/{}".format(start_date, end_date, apps_log_path, temp_file)
    return run(search_str, stderr=sys.stdout)


def dl_log(temp_file, logs_dir):
    return get('/tmp/' + temp_file, logs_dir)


def check_files(temp_file, logs_dir):
    remote_check = run('test -r /tmp/{} && echo ok'.format(temp_file))
    if (remote_check.strip() == 'ok') and os.path.isfile(os.path.join(logs_dir, temp_file)):
        print "log download success"
        if os.path.getsize(os.path.join(logs_dir, temp_file)) > 2:
            return 2
        else:
            return 1
    else:
        print "log not download"
        return False


def rm_remote_tempfile(temp_file):
    return run('rm -f /tmp/{}'.format(temp_file))


@task
def get_log(start_date, end_date, temp_file, apps_log_path):
    logs_dir = 'static/logs'
    if cut_log(start_date, end_date, temp_file, apps_log_path) == 0:
        if dl_log(temp_file, logs_dir) == 0:
            if check_files(temp_file, logs_dir) == 2:
                rm_remote_tempfile(temp_file)
                return True

