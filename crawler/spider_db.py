from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from crawler.models import Base, IndexedPagesTable, IndexedMediaTable

engine = create_engine('sqlite:///crawler_data.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
db_session = Session()


# @TODO add check for visited, but not indexed page (empty tags)
def is_url_indexed(url, table):
    return len(db_session.query(table).filter(table.url == url).all()) > 0
