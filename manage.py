import logging

from flask_script import Manager, Command, Option, Server
from app import create_app


app = create_app()
manager = Manager(app)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

if __name__ == 'main':
    manager.run()

