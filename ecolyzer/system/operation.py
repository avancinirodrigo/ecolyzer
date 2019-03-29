from sqlalchemy import Column, Integer, ForeignKey
#from sqlalchemy.orm import relationship, backref
#from ecolyzer.dataaccess import Base
from .code_element import CodeElement

class Operation(CodeElement):
	"""Operation"""
	__tablename__ = 'operation'
	__mapper_args__ = {'polymorphic_identity':'operation'}

	id = Column(None, ForeignKey('code_element.id'), primary_key=True)
