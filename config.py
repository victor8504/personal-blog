import os

class Config:
    SECRET_KEY = 'vnju'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql+psycopg2://victor:vnju@localhost/blog')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    # email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql+psycopg2://victor:vnju@localhost/blog')    

class ProdConfig(Config):
    # pass
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql+psycopg2://victor:vnju@localhost/blog')

class DevConfig(Config):
    DEBUG = True

config_options = {
    'development':DevConfig,
    'testing':TestConfig,
    'production':ProdConfig
}