# Some utility/context related functions for tests.

import unittest
from pypers import db


# Clean the database
def clean_db():
    db.DB.drop_tables(db.TABLES)
    db.DB.create_tables(db.TABLES)


# A lot of tests need the database to be initialized. This is done
# more easily by just extending this class
class _with_db(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        db._db_setup(':memory:', safe_create_tables=False)
