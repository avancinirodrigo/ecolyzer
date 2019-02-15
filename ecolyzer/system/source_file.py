from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from ecolyzer.dataaccess import Base

class SourceFile(Base):
	"""SourceFile"""
	__tablename__ = 'source_file'

	id = Column(Integer, primary_key=True)
	ext = Column(String)
	file_id = Column(Integer, ForeignKey('file.id'))
	file = relationship('File', backref=backref('source_file'))

	def __init__(self, file):
		self.file = file
		self.ext = file.ext
