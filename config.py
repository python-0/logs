class BaseConfig(object):
	'Base config class'

class DevlopmentConfig(BaseConfig):
	'Development environment specific config'
	DEBUG = True
	TESTING = True
	LOGS_DIR = 'static/logs'
	
	PAYMENT = {"node2": "/opt/catalina.out"}

class ProductionConfig(BaseConfig):
	'Production environment specific config'

config = {
	'development': DevlopmentConfig,
	'production': ProductionConfig
}
