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
		self.operations = {}

	def add_operation(self, operation):
		if operation.name not in self.operations: 
			operation.source_file = self
			self.operations[operation.name] = operation
		else:
			raise ValueError('Operation \'{0}\' is already present'.format(operation.name))

	def operation_exists(self, name):
		return name in self.operations

	def get_operation(self, name):
		return self.operations[name]	
