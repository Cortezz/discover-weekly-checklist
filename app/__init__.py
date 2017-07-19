import os

from logging import StreamHandler
from flask import Flask
from flask_login import LoginManager

from config import config
from app.database import db
from app.finders.user_finder import UserFinder

def create_app(config_name=None):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    login_manager = LoginManager(app)

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

    from app.views import discover_weekly
    app.register_blueprint(discover_weekly)

    login_manager.login_view = "discover_weekly.login"
    login_manager.user_loader(UserFinder.get_from_id)
    login_manager.login_message_category = 'info'
    login_manager.needs_refresh_message_category = 'info'

    app.app_context().push()
    return app