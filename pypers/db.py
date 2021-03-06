import peewee as pw
import datetime
from . import logger

_DEFAULT_PRAGMAS = (('foreign_keys', 'on'),)
DB = pw.SqliteDatabase(None, pragmas=_DEFAULT_PRAGMAS)
log = logger.logger_for(__name__)


# For the sake of testing, connecting to the database is deferred
# until runtime.
def _db_setup(database, safe_create_tables=True):
    DB.init(database)
    DB.create_tables(TABLES, safe=safe_create_tables)  # should be safe, right?


# A base model that all other models extend. Means we don't have to
# explicitly write the Meta class on every new Model.
class BaseModel(pw.Model):
    class Meta:
        database = DB


class _Paper(BaseModel):
    title = pw.CharField(255)  # Only the title should be required (?)
    pub_year = pw.DateField(formats='%Y', null=True)
    paper_hash = pw.CharField(64, null=True)
    pages = pw.IntegerField(null=True)
    url = pw.CharField(255, null=True)

    # Location on local filesystem.
    fs_location = pw.CharField(255, null=True)


# One-One relation between _Paper and _PaperMetaData (the latter of
# which also encompasses the relation)
class _PaperMetaData(BaseModel):
    bookmark = pw.IntegerField(default=0)
    date_added = pw.DateField(default=datetime.datetime.now())
    recently_added = pw.BooleanField(default=True)
    paper = pw.ForeignKeyField(_Paper, unique=True)


class _Author(pw.Model):
    firstname = pw.CharField(255)
    lastname = pw.CharField(255)

    middlenames = pw.CharField(255, null=True)

    class Meta:
        database = DB
        # Constrain `firstname' `lastname' to be unique
        indexes = ((('firstname', 'lastname'), True),)


class _Tag(BaseModel):
    name = pw.CharField(255, unique=True)
    description = pw.TextField(null=True)


# Many-Many relation between _Tag and _Paper
class _PaperTag(BaseModel):
    tag = pw.ForeignKeyField(_Tag)
    paper = pw.ForeignKeyField(_Paper)


# Many-Many relation between _Author and _Paper
class _PaperAuthor(BaseModel):
    author = pw.ForeignKeyField(_Author)
    paper = pw.ForeignKeyField(_Paper)


# Many-Many relation between _Paper and _Paper
class _Citation(BaseModel):
    paper = pw.ForeignKeyField(_Paper)
    citation = pw.ForeignKeyField(_Paper, related_name='cites')


TABLES = [
    _Paper,
    _PaperMetaData,
    _Author,
    _Tag,
    _PaperTag,
    _PaperAuthor,
    _Citation
]


# Helper for creating the various join operations. Returns a function
# that joins `source_t` on `on_t` using `rel_t` as the many-many
# relation.
def _many_many_join(reltable, idname, sourcetable, ontable):
    log.debug(f'Many many join on {reltable}')

    def q(x):
        sq = (sourcetable.select()
              .join(reltable)
              .join(ontable)
              .where(getattr(reltable, idname) == x.id))
        for e in sq:
            yield e
    return q


papers_of_author = _many_many_join(_PaperAuthor, "author_id", _Paper, _Author)
authors_of_paper = _many_many_join(_PaperAuthor, "paper_id", _Author, _Paper)

tags_of_paper = _many_many_join(_PaperTag, "paper_id", _Tag, _Paper)
papers_with_tag = _many_many_join(_PaperTag, "tag_id", _Paper, _Tag)
