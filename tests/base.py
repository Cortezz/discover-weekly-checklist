from unittest import TestCase

from app import create_app
from app.database import db, create_tables, drop_tables


class BaseTestCase(TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.test_app = self.app.test_client()
        create_tables()

    def tearDown(self):
        db.session.close()
        drop_tables()
