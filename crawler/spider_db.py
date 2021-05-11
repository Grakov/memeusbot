import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from crawler.models import Base, IndexedPagesTable, IndexedMediaTable
import crawler.crawler_settings as settings

engine = create_engine('sqlite:///' + os.path.join(settings.LOCAL_FOLDER, 'crawler_data.db'))
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
db_session = Session()


def is_url_indexed(url, table):
    return len(db_session.query(table).filter(table.url == url).all()) > 0
