import os
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from ecolyzer.dataaccess import Base

class File(Base):
	"""File"""
	__tablename__ = 'file'

	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	path = Column(String)
	ext = Column(String)
	system_id = Column(Integer, ForeignKey('system.id'))
	system = relationship('System', backref=backref('file'))	

	def __init__(self, fullpath):
		path, file_with_ext = os.path.split(fullpath)
		filename = ''
		ext = ''
		if '.' in file_with_ext:
			split_list = file_with_ext.split('.')
			if len(split_list) > 2:
				ext = split_list.pop()
				filename = '.'.join(split_list)
			else:
				if file_with_ext.startswith('.'):
					filename = '.' + split_list[1]
				else:
					filename = split_list[0]
					ext = split_list[1]
		else:
			filename = file_with_ext
		self.path = path
		self.name = filename
		self.ext = ext

	@property
	def path(self):
		return self._path

	@path.setter
	def path(self, path):
		self._path = path

	def fullpath(self):
		if self.ext == '':
			if self.path == '':
				return self.name
			else:
				return self.path + self.name
		elif self.path == '':
			return self.name + '.' + self.ext
		return self.path + '/' + self.name + '.' + self.ext
