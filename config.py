import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True

class Config:
    SECRET_KEY = '1A3KejYI1yC8o8HN'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    POSTS_PER_PAGE = 10
    #mail setting
    MAIL_SERVER = 'smtp.erongdu.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'services@erongdu.com'
    MAIL_PASSWORD = 'Service123'

    prv_key_path = os.path.join(basedir,'server_key')
    sql_file_path = os.path.join(basedir,'dbfile')

    @staticmethod
    def init_app(app):
        pass

class ProductionConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql://opsmanager:opsmanager_rd@127.0.0.1/opsmanager?charset=utf8'

config = {
    'production': ProductionConfig,
    'default': ProductionConfig
}
