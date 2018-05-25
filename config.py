import os

class Config:
    SECRET_KEY = 'vnju'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql+psycopg2://victor:vnju@localhost/blog')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class ProdConfig(Config):
    # pass
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql+psycopg2://victor:vnju@localhost/blog')

class DevConfig(Config):
    DEBUG = True

config_options = {
    'development':DevConfig,
    'production':ProdConfig,
}