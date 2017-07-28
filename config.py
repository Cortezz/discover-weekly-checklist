import os
import logging

from dotenv import load_dotenv


log = logging.getLogger(__name__)

if os.path.isfile('.env'):
    load_dotenv('.env')


class BaseConfig(object):

    DEBUG = False
    TESTING = False

    CLIENT_ID = os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
    SPOTIFY_SECRET = os.environ.get('SPOTIFY_USER')
    SECRET_KEY = os.environ.get('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @classmethod
    def init_app(cls, app):
        pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True

    @classmethod
    def init_app(cls, app):
        super(DevelopmentConfig, cls).init_app(app)


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = BaseConfig.SQLALCHEMY_DATABASE_URI + '_test'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}


