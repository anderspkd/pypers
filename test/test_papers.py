# Tests for the objects relating to papers, authors and so on.

from pypers import papers
from pypers import db  # for now this is needed

import papers_for_testing as _pft
from context import unittest, clean_db, _with_db


def make_author1():
    return papers.Author(_pft.author1['firstname'], _pft.author1['lastname'])


def make_author2():
    return papers.Author(_pft.author2['firstname'], _pft.author2['lastname'])


class TestAuthorObjects(_with_db):

    # Making multiple `Author' objects with the same author, doesn't
    # raise an error, since it returns the same underlying object.
    def test_make_multiple_same_author(self):

        a = make_author1()
        b = make_author1()

        self.assertNotEqual(a, b, 'is supposed to be different objects')
        self.assertEqual(a._db_obj, b._db_obj, 'is supposed to be the same')


class TestPaperObjects(_with_db):

    # Simple test. No authors. Essentially the same test
    # as(('firstname', 'lastname'), True)
    # test_make_multiple_same_author.
    def test_make_paper(self):

        paper1 = papers.Paper(
            _pft.paper1['title'],
            pages=_pft.paper1['pages'],
            file_hash=_pft.paper1['hash']
        )

        paper2 = papers.Paper(
            _pft.paper1['title'],
            pages=_pft.paper1['pages'],
            file_hash=_pft.paper1['hash']
        )

        self.assertNotEqual(
            paper1, paper2,
            'is supposed to be different'
        )
        self.assertEqual(
            paper1._db_obj, paper2._db_obj,
            'is supposed to be the same'
        )

    @clean_db
    def test_make_paper_and_get_metadata(self):
        paper = papers.Paper(
            _pft.paper1['title'],
            pages=_pft.paper1['pages'],
            file_hash=_pft.paper1['hash']
        )

        self.assertEqual(paper.bookmark, 0, 'bookmark should be 0')

        paper.bookmark = 10

        self.assertEqual(paper.bookmark, 10, 'bookmark should be 10')

        # This is to test that the actual database object is also
        # getting set correctly.
        m = db._PaperMetaData.get(db._PaperMetaData.paper == paper._db_obj)
        self.assertEqual(m.bookmark, 10, 'bookmark (in DB) should be 10')
        self.assertEqual(
            m.bookmark, paper.bookmark,
            'bookmark (in DB) should equal bookmark of paper object'
        )

    # test that we can iterate through the authors of a paper.
    def test_make_paper_with_authors(self):

        author1 = make_author1()
        author2 = make_author2()

        paper = papers.Paper(
            _pft.paper1['title'],
            pages=_pft.paper1['pages'],
            file_hash=_pft.paper1['hash'],
            authors=[author1, author2]
        )

        for author in paper.authors:
            self.assertIsNotNone(author)

    def test_create_author_from_string(self):
        # create an author from a string
        author1_str = _pft.author1_str
        author1_from_str = papers.Author.from_string(author1_str)
        author1 = make_author1()

        self.assertEqual(author1_from_str._db_obj, author1._db_obj)
        self.assertNotEqual(author1_from_str, author1)

        author2_str = _pft.author2_str
        author2_from_str = papers.Author.from_string(author2_str)
        author2 = make_author2()

        self.assertEqual(author2_from_str._db_obj, author2._db_obj)
        self.assertNotEqual(author2_from_str, author1)

    def test_authors_yields_papers(self):
        p = papers.Paper(
            _pft.paper1['title'],
            authors=[_pft.author1_str, _pft.author2_str]
        )
        a = papers.Author.from_string(_pft.author1_str)

        self.assertEqual(len(a.papers), 1)
        self.assertEqual(a.papers[0]._db_obj, p._db_obj)

    # we should be able to add authors by just adding a string. The
    # paper object should take care of creating the database entries
    def test_make_paper_with_authors_by_string(self):
        # Create paper with author from a paper object.
        author2 = make_author2()
        p = papers.Paper(
            _pft.paper2['title'],
            authors=[author2]
        )
        # Create paper with author from a string.
        author_str = _pft.author2_str
        p_str = papers.Paper(
            _pft.paper2['title'],
            authors=[author_str]
        )

        # The two papers should use the same author object.
        a = p.authors
        b = p_str.authors

        self.assertEqual(len(p.authors), len(p_str.authors))

        # Note that this also enforces the order of the authors.
        for aa, bb in zip(a, b):
            self.assertEqual(aa._db_obj, bb._db_obj)


if __name__ == '__main__':
    unittest.main()
