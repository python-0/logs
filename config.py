class BaseConfig(object):
    """ Base config class """


class DevlopmentConfig(BaseConfig):
    """ Development environment specific config """
    DEBUG = True
    TESTING = True
    LOGS_DIR = 'static/logs'
    MYSQL_HOST = 'mysql'
    MYSQL_USER = 'logs'
    MYSQL_PASSWORD = 'logs'
    MYSQL_DB = 'logs'
    MYSQL_PORT = 3306

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
