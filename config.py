import os
import logging

log = logging.getLogger(__name__)

class BaseConfiguration(object):
    CLIENT_ID = os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

