from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import engine
from sqlalchemy_utils import database_exists, create_database, drop_database

class SQLAlchemyEngine:
	_instance = None

	def __new__(cls):
		if cls._instance is None:
			cls._instance = object.__new__(cls)

		return cls._instance

	def create_engine(self, url):
		self.engine = create_engine(url)
		Session = sessionmaker(bind=self.engine)

	def createdb(self, url, overwrite):
		if database_exists(url):
			if overwrite:
				drop_database(url)
				create_database(url)
			else:
				url = engine.url.make_url(url)
				raise Exception('Database \'{}\' already exists.'.format(url.database))
		else:
			create_database(url)

	def existsdb(self, url):
		return database_exists(url)

	def dropdb(self, url):
		drop_database(url)

Base = declarative_base()
