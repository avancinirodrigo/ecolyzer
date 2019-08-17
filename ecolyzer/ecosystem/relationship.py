from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from ecolyzer.dataaccess import Base
#from .ecosystem import Ecosystem

class Relationship(Base):
	"""Relationship"""
	__tablename__ = 'relationship'

	id = Column(Integer, primary_key=True)

	from_system_id = Column(Integer, ForeignKey('system.id'))
	from_system = relationship('System', foreign_keys=[from_system_id])
	from_source_file_id = Column(Integer, ForeignKey('source_file.id'))
	from_source_file = relationship('SourceFile', foreign_keys=[from_source_file_id])
	from_code_element_id = Column(Integer, ForeignKey('code_element.id'))
	from_code_element = relationship('CodeElement', foreign_keys=[from_code_element_id])
	from_author_id = Column(Integer, ForeignKey('author.id'))
	from_author = relationship('Author', foreign_keys=[from_author_id]) 

	to_system_id = Column(Integer, ForeignKey('system.id'))
	to_system = relationship('System', foreign_keys=[to_system_id])
	to_source_file_id = Column(Integer, ForeignKey('source_file.id'))
	to_source_file = relationship('SourceFile', foreign_keys=[to_source_file_id])
	to_code_element_id = Column(Integer, ForeignKey('code_element.id'))
	to_code_element = relationship('CodeElement', foreign_keys=[to_code_element_id])		
	to_author_id = Column(Integer, ForeignKey('author.id'))
	to_author = relationship('Author', foreign_keys=[to_author_id]) 

	ecosystem_id = Column(Integer, ForeignKey('ecosystem.id'))
	
	def __init__(self, from_info, to_info):
		self.from_system = from_info.system
		self.from_source_file = from_info.source_file
		self.from_code_element = from_info.code_element
		self.from_author = from_info.author
		self.to_system = to_info.system
		self.to_source_file = to_info.source_file
		self.to_author = to_info.author
		self.to_code_element = to_info.code_element		

class RelationInfo():
	"""RelationInfo"""
	def __init__(self, system, source_file, code_element):
		self.system = system
		self.source_file = source_file
		self.code_element = code_element
		self.author = code_element.author()				


