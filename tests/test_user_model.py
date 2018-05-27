import unittest
from app.models import User

class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = User(password = 'cow')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password = 'cow')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User (password = 'cow')
        self.assertTrue(u.verify_password('cow'))
        self.assertFalse(u.verify_password('donkey'))

    def test_password_hashes_are_random(self):
        u = User(password = 'cow')
        u2 = User(password = 'cow')
        self.assertTrue(u.password_hash != u2.password_hash)