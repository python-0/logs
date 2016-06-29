import time

def get_unix_time():
	now = time.time()
	return str(now).replace('.','')
