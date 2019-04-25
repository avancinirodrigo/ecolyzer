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
	_fullpath = Column('fullpath', String, nullable=False, unique=True)
	system_id = Column(Integer, ForeignKey('system.id'))
	system = relationship('System', backref=backref('file'))	

	def __init__(self, fullpath):
		self.fullpath = fullpath

	@property
	def path(self):
		return self._path

	@path.setter
	def path(self, path):
		self._path = path
		self.fullpath = self._make_fullpath()
		
	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, name):
		self._name = name	
		self.fullpath = self._make_fullpath()
		
	@property
	def ext(self):
		return self._ext

	@ext.setter
	def ext(self, ext):
		self._ext = ext	
		self.fullpath = self._make_fullpath()

	@property # TODO: how to handle fullpath if change it?
	def fullpath(self):
		return self._fullpath	
		
	@fullpath.setter
	def fullpath(self, fullpath):
		if fullpath == None:
			return 
		self._fullpath = None	
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
		self._fullpath = fullpath

	def _make_fullpath(self):
		if self._fullpath == None:
			return
		elif self.ext == '':
			if self.path == '':
				return self.name
			else:
				return self.path + self.name
		elif self.path == '':
			return self.name + '.' + self.ext
		return self.path + '/' + self.name + '.' + self.ext
