import time
from wtforms.fields.html5 import DateField
from flask_wtf import Form

class DatePicker(Form):
	dt = DateField('datePicker', format='%Y-%m-%d %H:%M')

def get_unix_time():
	now = time.time()
	return str(now).replace('.', '')
