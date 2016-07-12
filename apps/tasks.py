import subprocess
import os
from apps import celery
from utils import get_unix_time


@celery.task
def add(x, y):
    return x + y


@celery.task
def get_logs(project, host, log_path, start_date, end_date, user_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print '/usr/local/bin/fab -f {}/get_logs.py -H {} \
    				get_log:start_date={},end_date={},temp_file={},apps_log_path={}' \
                    .format(os.path.join(current_dir, 'main'), host, start_date, end_date,
                            project + get_unix_time() + ".log",
                            log_path)

    result = subprocess.call('/usr/local/bin/fab -f {}/get_logs.py -H {} \
    				get_log:start_date={},end_date={},temp_file={},apps_log_path={}' \
                    .format(os.path.join(current_dir, 'main'), host, start_date,
                            end_date,
                            project + get_unix_time() + ".log",
                            log_path), shell=True)

    if result == 0:
        print "get logs success!"
