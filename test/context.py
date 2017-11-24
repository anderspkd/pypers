# Some utility/context related functions for tests.

import unittest
from pypers import db


# A lot of tests need the database to be initialized. This is done
# more easily by just extending this class
class _with_db(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        db._db_setup(':memory:', safe_create_tables=False)


# Decorator that ensures a clean database is used for a test
def clean_db(func):
    def f(*args, **kwargs):
        db.DB.drop_tables(db.TABLES)
        db.DB.create_tables(db.TABLES)
        func(*args, **kwargs)

    return f
