from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from ecolyzer.dataaccess import Base

class CodeElement(Base):
	"""CodeElement"""
	__tablename__ = 'code_element'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	type = Column(String)
	source_file_id = Column(Integer, ForeignKey('source_file.id'))
	source_file = relationship('SourceFile', backref=backref('code_element', 
											cascade='all,delete'))
	modification_id = Column(Integer, ForeignKey('modification.id'))
	modification = relationship('Modification', backref=backref('code_element',
		 									cascade='all,delete'))

	__mapper_args__ = {'polymorphic_on':type}	

	def __init__(self, name, source_file=None, modification=None):
		self.name = name
		self.source_file = source_file
		self.modification = modification

	def author(self):
		return self.modification.author()
		
