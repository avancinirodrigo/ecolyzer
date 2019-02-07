import os
from sqlalchemy import Column, String, Integer
from ecolyzer.dataaccess import Base

class File(Base):
	"""File"""
	__tablename__ = 'file'

	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	path = Column(String)
	ext = Column(String)
	fullpath = Column(String, nullable=False, unique=True)

	def __init__(self, fullpath):
		path, file_with_ext = os.path.split(fullpath)
		filename = ''
		ext = ''
		if '.' in file_with_ext:
			filename, ext = file_with_ext.split('.')
		else:
			filename = file_with_ext
		self.fullpath = fullpath
		self.path = path
		self.name = filename
		self.ext = ext
