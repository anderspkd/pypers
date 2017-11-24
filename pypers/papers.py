# This module contains classes that create direct mappings between the
# database (paper, author, and so on) objects.

from . import db


class Paper:

    # Only the title is required. Everything else is optional. The
    # more data supplied, the more "sure" we can be, that find a
    # potential duplicate in the database.
    def __init__(
            self,
            title,
            pages=None,
            file_hash=None,
            authors=None,
            year=None
    ):
        self.title = title
        self.pages = pages
        self.file_hash = file_hash
        self.authors = authors
        self.year = year

        try:
            p = db._Paper.get(db._Paper.title == self.title)
            self._db_obj = p
        except db._Paper.DoesNotExist:
            self._db_obj = db._Paper(title=self.title)
            self._db_obj.save()
            self._setup_metadata()

    # Create new PaperMetaData entry for this paper.
    def _setup_metadata(self):
        db._PaperMetaData(paper=self._db_obj).save()

    def _set_bookmark(self, new_bookmark):
        q = db._PaperMetaData.update(bookmark=new_bookmark).where(db._PaperMetaData.paper==self._db_obj)
        q.execute()

    def _get_bookmark(self):
        return db._PaperMetaData.get(db._PaperMetaData.paper == self._db_obj).bookmark

    bookmark = property(_get_bookmark, _set_bookmark)


class Author:

    def __init__(self, firstname, lastname, middlenames=None):
        self.firstname = firstname
        self.lastname = lastname

        try:
            a = db._Author.get(db._Author.firstname == self.firstname and
                               db._Author.lastname == self.lastname)
            self._db_obj = a
        except db._Author.DoesNotExist:
            self._db_obj = db._Author(firstname=self.firstname, lastname=self.lastname)
            self._db_obj.save()


class Tag:
    pass
