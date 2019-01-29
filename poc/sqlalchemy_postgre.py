from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database

engine = create_engine('postgresql://postgres:postgres@localhost:5432/sqlalchemy')
if database_exists(engine.url):
	drop_database(engine.url)

create_database(engine.url)

Session = sessionmaker(bind=engine)
Base = declarative_base()

from sqlalchemy import Column, String, Integer, Date

class Movie(Base):
    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

from datetime import date

Base.metadata.create_all(engine)
session = Session()
bourne_identity = Movie("The Bourne Identity", date(2002, 10, 11))
session.add(bourne_identity)
session.commit()
session.close()
drop_database(engine.url)