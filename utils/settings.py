import peewee_async
import peewee
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

settings = {
    "debug": True,
    "widgets_path": os.path.join(BASE_DIR, "widgets"),
    "assets_path": os.path.join(BASE_DIR, 'assets')
}

#sync_db = peewee.MySQLDatabase(**DATABASES)
#async_db = peewee_async.MySQLDatabase(**DATABASES)
sync_db = peewee.SqliteDatabase(os.path.join(BASE_DIR, "db.sqlite3"), pragmas={'journal_mode': 'wal'})
