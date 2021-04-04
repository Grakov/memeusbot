from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from crawler.models import IndexedPagesTable, IndexedMediaTable, Base

engine = create_engine('sqlite:///crawler_data.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
db_session = Session()


def check_indexed_url(url, table):
    return len(db_session.query(table).filter(table.url == url).all()) > 0
