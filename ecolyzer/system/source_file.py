from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from ecolyzer.dataaccess import Base

class SourceFile(Base):
	"""SourceFile"""
	__tablename__ = 'source_file'

	id = Column(Integer, primary_key=True)
	ext = Column(String)
	file_id = Column(Integer, ForeignKey('file.id'))
	file = relationship('File', backref=backref('source_file', uselist=False))

	def __init__(self, file):
		self.file = file
		self.ext = file.ext
		self.functions = {}

	def add_function(self, function):
		if function.name not in self.functions: 
			function.source_file = self
			self.functions[function.name] = function
		else:
			raise ValueError('Function \'{0}\' is already present'.format(function.name))

	def function_exists(self, name):
		return name in self.functions

	def get_function(self, name):
		return self.functions[name]	
