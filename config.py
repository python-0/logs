class BaseConfig(object):
    """ Base config class """
    CELERY_BROKER_URL = 'redis://redis:6379/0'
    CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
    BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
    LOGS_DIR = 'static/logs'

    @classmethod
    def init(cls, app):
        pass


class DevlopmentConfig(BaseConfig):
    """ Development environment specific config """
    DEBUG = True
    SECRET_KEY = 'xiaoer'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://logs:logs@mysql/logs'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    APPS_LOGS = {
        "wechat": {
            "node1": "/opt/catalina.out",
            "node2": "/opt/catalina.out",
            "node4": "/opt/catalina.out"
        },
        "payment": {
            "node2": "/opt/catalina.out"
        }
    }


class ProductionConfig(BaseConfig):
    """ Production environment specific config """


config = {
    'development': DevlopmentConfig,
    'production': ProductionConfig
}
