import pathlib
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.collections import attribute_mapped_collection
from ecolyzer.dataaccess import Base
from .code_element import CodeElement

class SourceFile(Base):
	"""SourceFile"""
	__tablename__ = 'source_file'

	id = Column(Integer, primary_key=True)
	file_id = Column(Integer, ForeignKey('file.id'), unique=True)
	file = relationship('File', backref=backref('source_file', uselist=False))
	system_id = Column(Integer, ForeignKey('system.id'))	
	_elements = relationship('CodeElement',
					collection_class=attribute_mapped_collection('key'))	

	def __init__(self, file):
		self.file = file

	def add_code_element(self, element):
		if not self.code_element_exists(element): 
	 		self._elements[element.key] = element
		else:
	 		raise ValueError('Code element \'{0}\' of type \'{1}\' is already present'
	 						.format(element.name, type(element).__name__))	 		

	def code_element_exists(self, element):
		return element.key in self._elements

	def code_element_by_key(self, key):
	 	return self._elements[key]

	def code_elements(self):
		return self._elements	

	def code_elements_len(self):
		return len(self._elements)

	@property
	def ext(self):
		return self.file.ext

	def name(self):
		return self.file.name

	def path(self):
		return self.file.path

	def fullpath(self):
		return self.file.fullpath		

	def system(self, system):
		self.file.system = system
	
	@property
	def source_code(self): #TODO: source code is in Modification		
		return open(str(pathlib.Path().absolute()) + '/' + self.file.fullpath).read()