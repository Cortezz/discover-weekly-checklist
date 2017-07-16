import os

from logging import StreamHandler
from dotenv import load_dotenv
from flask import Flask
from flask_oauthlib.client import OAuth

def create_app(config_object=None, db_name=None):
    app = Flask(__name__)
    load_dotenv(".env")

    if config_object is None:
        app.config.from_object('config.BaseConfiguration')
    else:
        app.config.from_object(config_object)

    if not app.logger.handlers:
        stream_handler = StreamHandler()
        app.logger.addHandler(stream_handler)

    if app.debug:
        app.logger.setLevel("DEBUG")
        app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
        app.config["DEBUG_TB_PROFILER_ENABLED"] = os.environ.get(
            "PROFILER", "False") == 'True'
        app.config['RQ_DEFAULT_URL'] = os.environ.get("REDIS_URL")
    else:
        app.logger.setLevel("DEBUG")


    from app.views import spotify_bp
    app.register_blueprint(spotify_bp)

    return app