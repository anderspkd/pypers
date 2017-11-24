# This module contains classes that create direct mappings between the
# database (paper, author, and so on) objects.

from . import db


# is thrown if Author.from_string fails to parse a name-string.
class AuthorNameParseException(Exception):
    pass


class Paper:

    # Only the title is required. Everything else is optional. The
    # more data supplied, the more "sure" we can be to find the paper
    # in our DB if it already exists.
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

    # Create new PaperMetaData entry for this paper. Not all
    # attributes makes sense to keep track off. For example, a
    # bookmark is likely to get updated, whereas the date a paper was
    # added, is not.
    def _setup_metadata(self):
        pm = db._PaperMetaData(paper=self._db_obj)
        self.date_added = pm.date_added
        self.is_new = pm.recently_added
        pm.save()

    # Setter/Getter for the bookmark. It is important that this is
    # updated each time we retrieve it, since we might have two
    # objects that represent the same paper.
    def _set_bookmark(self, new_bookmark):
        q = db._PaperMetaData.update(bookmark=new_bookmark)
        q = q.where(db._PaperMetaData.paper == self._db_obj)
        q.execute()

    def _get_bookmark(self):
        return db._PaperMetaData.get(
            db._PaperMetaData.paper == self._db_obj
        ).bookmark

    bookmark = property(_get_bookmark, _set_bookmark)


class Author:

    # Create an Author object from a single string. Two (simple) rules
    # are employed. If namestr contains a ',', then it's lastname
    # first and firstname last. Otherwise, everything before the first
    # space is firstname and everything after is lastname.
    @classmethod
    def from_string(cls, namestr):
        names = namestr.split(',')
        if len(names) == 2:
            lastname = names[0]
            firstname = names[1]
        else:
            names = namestr.split(' ')
            if len(names) > 1:
                firstname = names[0]
                lastname = ' '.join(names[1:])
            else:
                raise AuthorNameParseException(f'Invalid name "{namestr}"')

        return cls(firstname, lastname)

    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

        try:
            a = db._Author.get(db._Author.firstname == self.firstname and
                               db._Author.lastname == self.lastname)
            self._db_obj = a
        except db._Author.DoesNotExist:
            self._db_obj = db._Author(firstname=self.firstname,
                                      lastname=self.lastname)
            self._db_obj.save()


class Tag:
    pass
