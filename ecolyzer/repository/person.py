from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from ecolyzer.dataaccess import Base

class Person(Base):
	"""Person"""
	__tablename__ = 'person'	

	id = Column(Integer, primary_key=True)	
	name = Column(String, nullable=False)
	email = Column(String, nullable=False, unique=True)	
	
	def __init__(self, name, email):
		self.name = name
		self.email = email	
