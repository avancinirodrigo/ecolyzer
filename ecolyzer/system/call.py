from sqlalchemy import Column, String, ForeignKey
from .code_element import CodeElement

class Call(CodeElement):
	"""Call"""
	__tablename__ = 'call'
	__mapper_args__ = {'polymorphic_identity':'call'}

	id = Column(None, ForeignKey('code_element.id'), primary_key=True)
	# caller = Column(String)
	