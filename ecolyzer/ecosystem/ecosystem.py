from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship #, backref
#import sqlalchemy
from ecolyzer.dataaccess import Base
from .relationship import Relationship

class Ecosystem(Base):
	"""Ecosystem"""
	__tablename__ = 'ecosystem'

	id = Column(Integer, primary_key=True)
	# name = Column(String, nullable=False, unique=True)
	# repo_id = Column(Integer, ForeignKey('repository.id'))
	# repository = relationship('Repository', backref=backref('system', 
	# 				uselist=False, cascade='all,delete'))
	# source_files = relationship('SourceFile',
	# 				collection_class=attribute_mapped_collection('file.fullpath'))
	_relationships = relationship(Relationship) 
	# 				collection_class=attribute_mapped_collection('fullpath'))

#	def __init__(self):
#		self.relationships = []

	def add_relationship(self, relationship):
		if relationship not in self._relationships: 
	 		self._relationships.append(relationship)
		else:
	 		raise ValueError('Relationship TODO') # \'{0}\' of type \'{1}\' is already present'
	 						#.format(element.name, type(element).__name__))

	#def code_relationship_exists(self, relationship):
	#	return relationship in self._elements

	#def get_code_element_by_name(self, name):
	# 	return self._elements[name]	

	# def relationship_at(self, idx):
	# 	return self._relationships[idx]

	# def relationships_len(self):
	# 	return len(self.relationships)

	def relationships(self):
		return self._relationships
