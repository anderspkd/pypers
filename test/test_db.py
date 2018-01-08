from pypers import db

from papers_for_testing import *
from context import unittest, clean_db, _with_db


def _make_paper():
    p = db._Paper(
        title=paper1['title'],
        pub_year=paper1['year'],
        paper_hash=paper1['hash'],
        pages=paper1['pages']
    )
    return p


# This test really only reflects what the peewee interface looks
# like. It should not reflect how it is actually used
class TestDBbasic(_with_db):

    def test_Paper_insert(self):
        p = _make_paper()
        # insert should work
        self.assertEqual(p.save(), 1)
        p = db._Paper.get(db._Paper.pub_year == paper1['year'])
        # and we can extract the paper again
        self.assertEqual(p.title, paper1['title'])

    @clean_db
    def test_PaperMetaData_insert(self):

        # Not -strictly- needed. But we're testing database
        # primitives, so we kinda have to :-)

        # Create paper and save it (i.e., store it in the DB)
        p = _make_paper()
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

    @clean_db
    def test_Author_insert(self):
        a = db._Author(firstname=author1['firstname'],
                       lastname=author1['lastname'])
        self.assertEqual(a.save(), 1)
        # should be unique
        a = db._Author(firstname=author1['firstname'],
                       lastname=author1['lastname'])
        with self.assertRaises(db.pw.IntegrityError):
            a.save()

    @clean_db
    def test_Authors_unique_only_wrt_firstname_and_lastname1(self):
        # Test that two authors can have the same firstname
        a = db._Author(firstname=author1['firstname'],
                       lastname=author1['lastname'])
        self.assertEqual(a.save(), 1)
        a = db._Author(firstname=author1['firstname'],
                       lastname=author2['lastname'])
        self.assertEqual(a.save(), 1)
        self.assertEqual(db._Author.select().count(), 2)

    @clean_db
    def test_Authors_unique_only_wrt_firstname_and_lastname2(self):
        # Test that two authors can have the same lastname
        a = db._Author(firstname=author1['firstname'],
                       lastname=author1['lastname'])
        self.assertEqual(a.save(), 1)
        a = db._Author(firstname=author2['firstname'],
                       lastname=author1['lastname'])
        self.assertEqual(a.save(), 1)
        self.assertEqual(db._Author.select().count(), 2)


class TestDBQueries(_with_db):

    @clean_db
    def test_find_all_papers(self):
        p = db._Paper(title=paper1['title'])
        a1 = db._Author(firstname=author1['firstname'], lastname=author1['lastname'])
        a2 = db._Author(firstname=author2['firstname'], lastname=author2['lastname'])

        p.save()
        a1.save()
        a2.save()

        db._PaperAuthor(author=a1, paper=p).save()
        db._PaperAuthor(author=a2, paper=p).save()

        pp = next(db.papers_of_author(a1))
        self.assertEqual(p, pp)


if __name__ == '__main__':
    unittest.main()
