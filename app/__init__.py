import os

from logging import StreamHandler
from dotenv import load_dotenv
from flask import Flask

from config import config
from app.database import db

def create_app(config_name=None):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

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

    app.app_context().push()
    return app