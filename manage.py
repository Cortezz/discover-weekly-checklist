import logging
import os
import unittest

from flask_script import Manager, Command, Option, Server
from app import create_app

logging.info("Starting Logger for Discover Weekly Checklist")

app_env = os.environ.get('APP_ENV', 'development')
app = create_app(app_env)
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


@manager.command
def run_tests():
    tests = unittest.TestLoader().discover(start_dir='tests/', pattern='*_test.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == "__main__":
    manager.run()
