from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.collections import attribute_mapped_collection
from ecolyzer.dataaccess import Base

class System(Base):
	"""System"""
	__tablename__ = 'system'

	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False, unique=True)
	repo_id = Column(Integer, ForeignKey('repository.id'))
	repository = relationship('Repository', backref=backref('system', 
					uselist=False, cascade='all,delete'))
	source_files = relationship("SourceFile",
					collection_class=attribute_mapped_collection('file.fullpath'))
	files = relationship("File",
					collection_class=attribute_mapped_collection('fullpath'))

	def __init__(self, name, repository):
		self.name = name
		self.repository = repository

	def add_file(self, file):
		if file.fullpath not in self.files: 
			file.system = self
			self.files[file.fullpath] = file
		else:
			raise ValueError('File \'{0}\' is already present'.format(file.fullpath))

	def file_exists(self, fullpath):
		return fullpath in self.files

	def get_file(self, fullpath):
		if self.file_exists(fullpath):
			return self.files[fullpath]
		else:
			raise ValueError('File \'{0}\' not exists'.format(fullpath))	

	def remove_file(self, fullpath):
		del self.files[fullpath]

	def add_source_file(self, source_file):
		file = source_file.file
		if file.fullpath not in self.source_files: 
			self.source_files[file.fullpath] = source_file
		else:
			raise ValueError('Source file \'{0}\' is already present'.format(file.fullpath))

	def source_file_exists(self, fullpath):
		return fullpath in self.source_files

	def get_source_file(self, fullpath):
		if self.source_file_exists(fullpath):
			return self.source_files[fullpath]
		else:
			raise ValueError('Source file \'{0}\' not exists'.format(fullpath))	
			