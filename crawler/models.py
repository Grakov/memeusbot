from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class IndexedPagesTable(Base):
    __tablename__ = 'indexed_pages'
    url = Column(String, primary_key=True)
    tags = Column(String)
    alt_tags = Column(String)
    media = Column(String)

    def __repr__(self):
        return self.url


class IndexedMediaTable(Base):
    __tablename__ = 'indexed_media'
    url = Column(String, primary_key=True)
    id = Column(String)
    hash = Column(String)
    file_name = Column(String)
    tags = Column(String)
    alt_tags = Column(String)
    description = Column(String)
    meaning = Column(String)
    article_url = Column(String)

    def __repr__(self):
        return f"{self.url} ({self.hash})"
