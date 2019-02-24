from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from ecolyzer.dataaccess import Base

class Function(Base):
	"""Function"""
	__tablename__ = 'function'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	source_file_id = Column(Integer, ForeignKey('source_file.id'))
	source_file = relationship('SourceFile', backref=backref('function', 
											cascade='all,delete'))

	def __init__(self, name, source_file=None):
		self.name = name
		self.source_file = source_file
