from sqlalchemy import Column, String, Integer, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship, backref
from ecolyzer.dataaccess import Base
from .code_element import CodeElement

class SourceFile(Base):
	"""SourceFile"""
	__tablename__ = 'source_file'

	id = Column(Integer, primary_key=True)
	file_id = Column(Integer, ForeignKey('file.id'), unique=True)
	file = relationship('File', backref=backref('source_file', uselist=False))
	system_id = Column(Integer, ForeignKey('system.id'))	
	_elements = relationship(CodeElement)	

	def __init__(self, file):
		self.file = file

	def add_code_element(self, element):
		if element not in self._elements: 
	 		element.source_file = self
	 		self._elements.append(element)
		else:
	 		raise ValueError('Code element \'{0}\' of type \'{1}\' is already present'
	 						.format(element.name, type(element).__name__))

	def code_element_exists(self, element):
		return element in self._elements

	#def get_code_element_by_name(self, name):
	# 	return self._elements[name]	

	def code_element_at(self, idx):
		return self._elements[idx]

	def code_elements_len(self):
		return len(self._elements)

	def ext(self):
		return self.file.ext