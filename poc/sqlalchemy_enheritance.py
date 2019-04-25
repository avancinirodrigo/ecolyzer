from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from ecolyzer.dataaccess import Base

class Function(Base):
	"""Function"""
	__tablename__ = 'function'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	type = Column(String)
	source_file_id = Column(Integer, ForeignKey('source_file.id'))
	source_file = relationship('SourceFile', backref=backref('function', 
											cascade='all,delete'))
	__mapper_args__ = {'polymorphic_on':type}	

	def __init__(self, name, source_file=None):
		self.name = name
		self.source_file = source_file

class GlobalCall(Function):
	"""GlobalCall"""
	__tablename__ = 'global_call'
	__mapper_args__ = {'polymorphic_identity':'global_call'}

	id = Column(None, ForeignKey('function.id'), primary_key=True)

class Call(Function):
	"""Call"""
	__tablename__ = 'call'
	__mapper_args__ = {'polymorphic_identity':'call'}

	id = Column(None, ForeignKey('function.id'), primary_key=True)
	# caller = Column(String)
