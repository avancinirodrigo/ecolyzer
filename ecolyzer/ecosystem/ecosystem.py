from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship #, backref
from ecolyzer.dataaccess import Base
from .relationship import Relationship

class Ecosystem(Base):
	"""Ecosystem"""
	__tablename__ = 'ecosystem'

	id = Column(Integer, primary_key=True)
	_relationships = relationship(Relationship) 
	 	
	def add_relationship(self, relationship):
	 	self._relationships.append(relationship)
	
	@property 	
	def relationships(self):
		return self._relationships.copy()
