from sqlalchemy import Column, String, Integer
#from sqlalchemy.orm import relationship, backref
from ecolyzer.dataaccess import Base

class Repository(Base):
	"""Repository"""
	__tablename__ = 'repository'

	id = Column(Integer, primary_key=True)
	path = Column(String, nullable=False, unique=True)

	def __init__(self, path):
		self.path = path
		