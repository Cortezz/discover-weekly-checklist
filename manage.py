import logging

from flask_script import Manager, Command, Option, Server
from app import create_app

logging.info("Starting Logger for Discover Weekly Checklist")

app = create_app()
manager = Manager(app)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

if __name__ == "__main__":
    manager.run()