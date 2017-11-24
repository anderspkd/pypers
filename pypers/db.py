import peewee as pw
import datetime

_DEFAULT_PRAGMAS = (('foreign_keys', 'on'),)
DB = pw.SqliteDatabase(None, pragmas=_DEFAULT_PRAGMAS)


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


# Only the title should be required (?)
class _Paper(BaseModel):
    title = pw.CharField(255)
    pub_year = pw.DateField(formats='%Y', null=True)
    paper_hash = pw.CharField(64, null=True)
    pages = pw.IntegerField(null=True)
    url = pw.CharField(255, null=True)

    # Location on local filesystem.
    fs_location = pw.CharField(255, null=True)


class _PaperMetaData(BaseModel):
    bookmark = pw.IntegerField(default=0)
    date_added = pw.DateField(default=datetime.datetime.now())
    recently_added = pw.BooleanField(default=True)
    paper = pw.ForeignKeyField(_Paper, unique=True)


class _Author(pw.Model):
    # name = pw.CharField(255, unique=True)

    firstname = pw.CharField(255)
    lastname = pw.CharField(255)

    middlenames = pw.CharField(255, null=True)

    class Meta:
        database = DB
        indexes = ((('firstname', 'lastname'), True),)


class _Tag(BaseModel):
    name = pw.CharField(255, unique=True)
    description = pw.TextField(null=True)


class _PaperTag(BaseModel):
    tag = pw.ForeignKeyField(_Tag)
    paper = pw.ForeignKeyField(_Paper)


class _PaperAuthor(BaseModel):
    author = pw.ForeignKeyField(_Author)
    paper = pw.ForeignKeyField(_Paper)


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
