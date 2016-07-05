from fabric.api import task, run, get
import os


def cut_log(start_date, end_date, temp_file, apps_log_path):
    search_str = "sed -n '/{}/,/{}/p' {} > /tmp/{}".format(start_date, end_date, apps_log_path, temp_file)
    run(search_str)


def dl_log(temp_file, logs_dir):
    get('/tmp/' + temp_file, logs_dir)


def check_files(temp_file, logs_dir):
    remote_check = run('test -r /tmp/{} && echo ok'.format(temp_file))
    if (remote_check.strip() == 'ok') and os.path.isfile(os.path.join(logs_dir, temp_file)):
        print "log download success"
    else:
        print "log not download"


def rm_remote_tempfile(temp_file):
    run('rm -f /tmp/{}'.format(temp_file))


@task
def get_log(start_date, end_date, temp_file, apps_log_path):
    logs_dir = 'logs'
    cut_log(start_date, end_date, temp_file, apps_log_path)
    dl_log(temp_file, logs_dir)
    check_files(temp_file, logs_dir)
    rm_remote_tempfile(temp_file)
