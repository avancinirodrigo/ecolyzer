from sqlalchemy import Column, ForeignKey
from .code_element import CodeElement


class Operation(CodeElement):
	"""Operation"""
	__tablename__ = 'operation'
	__mapper_args__ = {'polymorphic_identity': 'operation'}

	id = Column(None, ForeignKey('code_element.id'), primary_key=True)
