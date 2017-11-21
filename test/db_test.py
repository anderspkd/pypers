import unittest
import db
from hashlib import sha256
from peewee import IntegrityError


class TestDBbasic(unittest.TestCase):

    def _cleanup_setup(self):
        db.DB.drop_tables(db.TABLES)
        db._db_setup()

    def setUp(self):
        db._db_init(':memory:')
        db._db_connect()
        db._db_setup()

    def tearDown(self):
        db.DB.drop_tables(db.TABLES)
        db._db_close()

    def _make_paper(self):
        p = db.Paper(
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
        p = db.Paper.get(db.Paper.pub_year == 2014)
        # and we can extract the paper again
        self.assertEqual(p.title, 'Universally Composable Authentication and Key-exchange with Global PKI')

    def test_PaperMetaData_insert(self):
        # Clean up database
        self._cleanup_setup()
        # Create paper and save it (i.e., store it in the DB)
        p = self._make_paper()
        p.save()
        # Create metadata object associated with the paper
        pmd1 = db.PaperMetaData(paper=p)
        pmd1_rows_inserted = pmd1.save()
        self.assertEqual(pmd1_rows_inserted, 1)

        pmd2 = db.PaperMetaData(paper=p)
        # Cannot have two MetaData objects for the same paper
        with self.assertRaises(IntegrityError):
            pmd2.save()

    def test_Author_insert(self):
        a = db.Author(name='Ran Canetti')
        self.assertEqual(a.save(), 1)
        # should be unique
        a = db.Author(name='Ran Canetti')
        with self.assertRaises(IntegrityError):
            a.save()




if __name__ == '__main__':
    unittest.main()
