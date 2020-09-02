from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from ecolyzer.dataaccess import Base
from .relationship import Relationship

class Ecosystem(Base):
	"""Ecosystem"""
	__tablename__ = 'ecosystem'

	id = Column(Integer, primary_key=True)
	_name = Column('name', String, unique=True)
	_relationships = relationship(Relationship) 
	 	
	def __init__(self, name: str=''):
		self._name = name

	@hybrid_property
	def name(self):
		return self._name
	
	def add_relationship(self, relationship):
	 	self._relationships.append(relationship)
	
	@property 	
	def relationships(self):
		return self._relationships.copy()
