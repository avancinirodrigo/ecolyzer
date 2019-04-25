from sqlalchemy import Column, String, Integer
from ecolyzer.dataaccess import Base

class Author(Base):
	"""Author"""
	__tablename__ = 'author'

	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False, unique=True)
	email = Column(String, nullable=False, unique=True)

	def __init__(self, name, email):
		self.name = name
		self.email = email
