import os
from decouple import config
from datetime import timedelta


BASE_DIR=os.path.dirname(os.path.realpath(__file__))

class Config:
    SECRET_KEY=config('SECRET_KEY', 'secret')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES= timedelta(minutes=30)
    JWT_SECRET_KEY=config('JWT_SECRET_KEY',)
    # SQLALCHEMY_TRACK_MODIFICATIONS=False


class DevConfig(Config):
    DEBUG=config('FLASK_DEBUG', cast=bool)
    # SQLALCHEMY_ECHO=False
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:Sefterli0506@localhost/flask_mesaj_db'



class TestConfig(Config):
    TESTING=True
    # SQLALCHEMY_ECHO=False
    SSQLALCHEMY_DATABASE_URI='postgresql://postgres:Sefterli0506@localhost/test_flask_mesaj_db'


class ProdConfig(Config):
    pass


config_dict = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'test': TestConfig

}