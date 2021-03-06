class BaseConfig(object):
    """ Base config class """


class DevlopmentConfig(BaseConfig):
    """ Development environment specific config """
    DEBUG = True
    SECRET_KEY = 'xiaoer'
    TESTING = True
    LOGS_DIR = 'static/logs'
    SQLALCHEMY_DATABASE_URI = 'mysql://logs:logs@mysql/logs'
    SQLALCHEMY_TRACK_MODIFICATIONS = 'True'

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
