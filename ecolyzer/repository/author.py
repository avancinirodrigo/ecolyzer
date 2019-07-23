from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from ecolyzer.dataaccess import Base

class Author(Base):
	"""Author"""
	__tablename__ = 'author'

	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	email = Column(String, nullable=False)
	repository_id = Column(Integer, ForeignKey('repository.id'))
	repository = relationship('Repository', backref=backref('author'))	

	def __init__(self, name, email):
		self.name = name
		self.email = email
