from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property
from ecolyzer.dataaccess import Base
from .person import Person

class Author(Base):
	"""Author"""
	__tablename__ = 'author'

	id = Column(Integer, primary_key=True)
	repository_id = Column(Integer, ForeignKey('repository.id'))
	repository = relationship('Repository', 
						backref=backref('author', cascade='all, delete-orphan'))	
	person_id = Column(Integer, ForeignKey('person.id'))
	person = relationship('Person', 
						backref=backref('author', cascade='all, delete-orphan'))		

	def __init__(self, person, repo=None):
		self.person = person
		self.repository = repo

	@hybrid_property
	def email(self):
		return self.person.email

	@hybrid_property
	def name(self):
		return self.person.name

	@name.setter
	def name(self, name):
		self.person.name = name				
