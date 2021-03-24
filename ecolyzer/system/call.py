from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.ext.hybrid import hybrid_property
from .code_element import CodeElement


class Call(CodeElement):
	"""Call"""
	__tablename__ = 'call'

	id = Column(None, ForeignKey('code_element.id'), primary_key=True)
	_caller = Column('caller', String)	
	__mapper_args__ = {'polymorphic_identity': 'call'}

	@hybrid_property
	def caller(self):
		return self._caller

	@caller.setter
	def caller(self, caller):
		self._caller = caller
