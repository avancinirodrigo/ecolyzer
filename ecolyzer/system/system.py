from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from ecolyzer.dataaccess import Base

class System(Base):
	"""System"""
	__tablename__ = 'system'

	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False, unique=True)
	repo_id = Column(Integer, ForeignKey('repository.id'))
	repository = relationship('Repository', backref=backref('system', 
							uselist=False, cascade='all,delete'))

	def __init__(self, name, repository):
		self.name = name
		self.repository = repository
		self.files = {}

	def add_file(self, file):
		if file.fullpath not in self.files: 
			file.system = self
			self.files[file.fullpath] = file
		else:
			raise ValueError('File \'{0}\' is already present'.format(file.fullpath))

	def file_exists(self, file_fullpath):
		return file_fullpath in self.files
