import unittest
from pypers import db
from hashlib import sha256


# This test really only reflects what the peewee interface looks
# like. It should not reflect how it is actually used
class TestDBbasic(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        db._db_setup(':memory:', safe_create_tables=False)

    # some tests require a clean database. In that case, use this
    # function
    def clean_db(self):
        db.DB.drop_tables(db.TABLES)
        db.DB.create_tables(db.TABLES)

    def _make_paper(self):
        p = db._Paper(
            title='Universally Composable Authentication and Key-exchange with Global PKI',
            pub_year=2014,
            paper_hash=sha256(b'1').hexdigest(),
            pages=30
        )
        return p

    def test_Paper_insert(self):
        p = self._make_paper()
        # insert should work
        self.assertEqual(p.save(), 1)
        p = db._Paper.get(db._Paper.pub_year == 2014)
        # and we can extract the paper again
        self.assertEqual(p.title, 'Universally Composable Authentication and Key-exchange with Global PKI')

    def test_PaperMetaData_insert(self):

        # Not -strictly- needed. But we're testing database
        # primitives, so we kinda have to :-)
        self.clean_db()

        # Create paper and save it (i.e., store it in the DB)
        p = self._make_paper()
        p.save()
        # Create metadata object associated with the paper
        pmd1 = db._PaperMetaData(paper=p)
        pmd1_rows_inserted = pmd1.save()
        self.assertEqual(pmd1_rows_inserted, 1)

        pmd2 = db._PaperMetaData(paper=p)
        # Cannot have two MetaData objects for the same paper
        with self.assertRaises(db.pw.IntegrityError):
            pmd2.save()

    def test_Author_insert(self):
        a = db._Author(name='Ran Canetti')
        self.assertEqual(a.save(), 1)
        # should be unique
        a = db._Author(name='Ran Canetti')
        with self.assertRaises(db.pw.IntegrityError):
            a.save()


if __name__ == '__main__':
    unittest.main()
