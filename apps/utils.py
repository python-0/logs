import time
from wtforms.fields.html5 import DateTimeField
from flask_wtf import Form
from datetime import datetime


class DatePicker(Form):
    dt = DateTimeField('dateTimePicker', format="%Y-%m-%dT%H:%M", default=datetime.today)


def get_unix_time():
    now = time.time()
    return str(now).replace('.', '')

