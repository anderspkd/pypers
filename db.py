import peewee as pw
import datetime

DB = None
_DEFAULT_PRAGMAS = (('foreign_keys', 'on'),)


# Some methods for delaying creation, connecting an so on.
def _db_init(database_name, pragmas=_DEFAULT_PRAGMAS):
    global DB
    DB = pw.SqliteDatabase(database_name, pragmas=pragmas)


def _db_setup(safe=True):
    DB.create_tables(TABLES, safe=safe)


def _db_connect():
    DB.connect()


def _db_close():
    DB.close()


# A base model that all other models extend. Means we don't have to
# explicitly write the Meta class on every new Model.
class BaseModel(pw.Model):
    class Meta:
        database = DB


class Paper(BaseModel):
    title = pw.CharField(255)
    pub_year = pw.DateField(formats='%Y')
    paper_hash = pw.CharField(64)
    pages = pw.IntegerField()
    url = pw.CharField(255, null=True)

    # Location on local filesystem.
    fs_location = pw.CharField(255, null=True)


class PaperMetaData(BaseModel):
    bookmark = pw.IntegerField(default=0)
    date_added = pw.DateField(default=datetime.datetime.now())
    recently_added = pw.BooleanField(default=True)
    paper = pw.ForeignKeyField(Paper, unique=True)


class Author(BaseModel):
    name = pw.CharField(255, unique=True)


class Tag(BaseModel):
    name = pw.CharField(255, unique=True)
    description = pw.TextField(null=True)


class PaperTag(BaseModel):
    tag = pw.ForeignKeyField(Tag)
    paper = pw.ForeignKeyField(Paper)


class PaperAuthor(BaseModel):
    author = pw.ForeignKeyField(Author)
    paper = pw.ForeignKeyField(Paper)


class Citation(BaseModel):
    paper = pw.ForeignKeyField(Paper)
    citation = pw.ForeignKeyField(Paper, related_name='cites')


TABLES = [
    Paper,
    PaperMetaData,
    Author,
    Tag,
    PaperTag,
    PaperAuthor,
    Citation
]
