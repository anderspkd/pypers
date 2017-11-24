from pypers import db

import papers_for_testing as _ptf
from context import unittest, clean_db, _with_db


# This test really only reflects what the peewee interface looks
# like. It should not reflect how it is actually used
class TestDBbasic(_with_db):

    def _make_paper(self):
        p = db._Paper(
            title=_ptf.paper1['title'],
            pub_year=_ptf.paper1['year'],
            paper_hash=_ptf.paper1['hash'],
            pages=_ptf.paper1['pages']
        )
        return p

    def test_Paper_insert(self):
        p = self._make_paper()
        # insert should work
        self.assertEqual(p.save(), 1)
        p = db._Paper.get(db._Paper.pub_year == _ptf.paper1['year'])
        # and we can extract the paper again
        self.assertEqual(p.title, _ptf.paper1['title'])

    def test_PaperMetaData_insert(self):

        # Not -strictly- needed. But we're testing database
        # primitives, so we kinda have to :-)
        clean_db()

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

    def test_what_happens_when_no_match(self):
        # `get' will raise an exception
        with self.assertRaises(db._Author.DoesNotExist):
            db._Author.get(db._Author.firstname == 'non existant author')

    def test_Author_insert(self):
        a = db._Author(firstname=_ptf.author1['firstname'],
                       lastname=_ptf.author1['lastname'])
        self.assertEqual(a.save(), 1)
        # should be unique
        a = db._Author(firstname=_ptf.author1['firstname'],
                       lastname=_ptf.author1['lastname'])
        with self.assertRaises(db.pw.IntegrityError):
            a.save()

    def test_Authors_unique_only_wrt_firstname_and_lastname(self):
        # Test that two authors can have the same firstname
        clean_db()
        a = db._Author(firstname=_ptf.author1['firstname'],
                       lastname=_ptf.author1['lastname'])
        self.assertEqual(a.save(), 1)
        a = db._Author(firstname=_ptf.author1['firstname'],
                       lastname=_ptf.author2['lastname'])
        self.assertEqual(a.save(), 1)
        self.assertEqual(db._Author.select().count(), 2)

        # Test that two authors can have the same lastname
        clean_db()
        a = db._Author(firstname=_ptf.author1['firstname'],
                       lastname=_ptf.author1['lastname'])
        self.assertEqual(a.save(), 1)
        a = db._Author(firstname=_ptf.author2['firstname'],
                       lastname=_ptf.author1['lastname'])
        self.assertEqual(a.save(), 1)
        self.assertEqual(db._Author.select().count(), 2)

if __name__ == '__main__':
    unittest.main()
