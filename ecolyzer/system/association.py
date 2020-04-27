from sqlalchemy import Column, String, ForeignKey
from .code_element import CodeElement

class Association(CodeElement):
	"""Association"""
	__tablename__ = 'association'
	__mapper_args__ = {'polymorphic_identity':'association'}

	id = Column(None, ForeignKey('code_element.id'), primary_key=True)
	