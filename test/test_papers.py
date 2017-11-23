# Tests for the objects relating to papers, authors and so on.

from pypers import papers
from pypers import db  # for now this is needed

import papers_for_testing as _pft
from context import unittest, clean_db, _with_db


class TestAuthorObjects(_with_db):

    # Making multiple `Author' objects with the same author, doesn't
    # raise an error, since it returns the same underlying object.
    def test_make_multiple_same_author(self):

        author1 = papers.Author(_pft.author1['name'])
        author2 = papers.Author(_pft.author1['name'])

        self.assertNotEqual(author1, author2, 'is supposed to be different objects')
        self.assertEqual(author1._db_obj, author2._db_obj, 'is supposed to be the same')


class TestPaperObjects(_with_db):

    # Simple test. No authors. Essentially the same test as
    # test_make_multiple_same_author.
    def test_make_paper(self):

        paper1 = papers.Paper(
            _pft.paper1['title'],
            pages = _pft.paper1['pages'],
            file_hash = _pft.paper1['hash']
        )

        paper2 = papers.Paper(
            _pft.paper1['title'],
            pages = _pft.paper1['pages'],
            file_hash = _pft.paper1['hash']
        )

        self.assertNotEqual(paper1, paper2, 'is supposed to be different')
        self.assertEqual(paper1._db_obj, paper2._db_obj, 'is supposed to be the same')

    def test_make_paper_and_get_metadata(self):

        clean_db()

        paper = papers.Paper(
            _pft.paper1['title'],
            pages = _pft.paper1['pages'],
            file_hash = _pft.paper1['hash']
        )

        self.assertEqual(paper.bookmark, 0, 'bookmark should be 0')

        paper.bookmark = 10

        self.assertEqual(paper.bookmark, 10, 'bookmark should be 10')

        # This is to test that the actual database object is also
        # getting set correctly.
        m = db._PaperMetaData.get(db._PaperMetaData.paper == paper._db_obj)
        self.assertEqual(m.bookmark, 10, 'bookmark (in DB) should be 10')
        self.assertEqual(m.bookmark, paper.bookmark,
                         'bookmark (in DB) should equal bookmark of paper object')

    # test that we can iterate through the authors of a paper.
    def test_make_paper_with_authors(self):

        author1 = papers.Author(_pft.author1['name'])
        author2 = papers.Author(_pft.author2['name'])

        paper = papers.Paper(
            _pft.paper1['title'],
            pages = _pft.paper1['pages'],
            file_hash = _pft.paper1['hash'],
            authors = [author1, author2]
        )

        for author in paper.authors:
            self.assertIsNotNone(author)


    # we should be able to add authors by just adding a string. The
    # paper object should take care of creating the database entries
    # def test_make_paper_with_authors_by_string(self):


if __name__ == '__main__':
    unittest.main()
