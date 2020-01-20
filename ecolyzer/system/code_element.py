from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from ecolyzer.dataaccess import Base

class CodeElement(Base):
	"""CodeElement"""
	__tablename__ = 'code_element'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	type = Column(String)
	key = Column(String)
	source_file_id = Column(Integer, ForeignKey('source_file.id'))
	source_file = relationship('SourceFile', backref=backref('code_element', 
											cascade='all,delete'))
	modification_id = Column(Integer, ForeignKey('modification.id'))
	modification = relationship('Modification', backref=backref('code_element',
		 									cascade='all,delete'))
	__table_args__ = (UniqueConstraint('id', 'key'),)
	__mapper_args__ = {'polymorphic_on':type}	

	def __init__(self, name, source_file, modification=None):
		self.name = name
		self.source_file = source_file
		self.modification = modification
		self.key = self.type + '_' + self.name + '_'

	def author(self):
		return self.modification.author()

	@property
	def source_code(self): #TODO: this is a hack, review
		return self.modification.source_code