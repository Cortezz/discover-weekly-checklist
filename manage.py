import logging

from flask_script import Manager, Command, Option, Server
from app import create_app

logging.info("Starting Logger for Discover Weekly Checklist")

app = create_app()
manager = Manager(app)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


@manager.command
def create_db():
    from app.database import create_tables
    create_tables()

@manager.command
def drop_db():
    from app.database import drop_tables
    drop_tables()

@manager.command
def reset_db():
    from app.database import create_tables, drop_tables
    drop_tables()
    create_tables()

if __name__ == "__main__":
    manager.run()