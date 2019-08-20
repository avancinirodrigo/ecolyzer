from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import engine
from sqlalchemy_utils import database_exists, create_database, drop_database

class SQLAlchemyORM:
	def  __init__(self, url):
		self.url = url

	def create_engine(self):
		self.engine = create_engine(self.url)
		self.session = sessionmaker(bind=self.engine)
		
	def create_all_tables(self):
		Base.metadata.create_all(self.engine)

	def create_all(self, overwrite=False):
		self.createdb(overwrite)
		self.create_engine()
		self.create_all_tables()		
		
	def create_session(self):
		return self.session()

	def createdb(self, overwrite=False):
		if database_exists(self.url):
			if overwrite:
				drop_database(self.url)
				create_database(self.url)
			else:
				url = engine.url.make_url(self.url)
				raise Exception('Database \'{}\' already exists.'.format(url.database))
		else:
			create_database(self.url)

	def existsdb(self):
		return database_exists(self.url)

	def dropdb(self):
		drop_database(self.url)

	def drop_all(self):
		Base.metadata.drop_all(self.engine)
		self.dropdb() 

Base = declarative_base()

class NullSession:
	"""NullSession"""
	def add(self, arg):
		pass
		
	def commit(self):
		pass