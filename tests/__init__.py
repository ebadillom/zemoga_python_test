import unittest

from main import app


class BaseTestClass(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
