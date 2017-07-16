import os
import logging

log = logging.getLogger(__name__)

class BaseConfiguration(object):
    DEBUG = os.environ.get("DEBUG_MODE") == "True"
    CLIENT_ID = os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
    SPOTIFY_SECRET = os.environ.get('SPOTIFY_USER')
    SECRET_KEY = os.environ.get('SECRET_KEY')