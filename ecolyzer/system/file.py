from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property
from ecolyzer.utils import FileUtils
from ecolyzer.dataaccess import Base


class File(Base):
	"""File"""
	__tablename__ = 'file'

	id = Column(Integer, primary_key=True)
	_name = Column('name', String, nullable=False)
	_path = Column('path', String)
	_ext = Column('ext', String)
	_fullpath = Column('fullpath', String, nullable=False)
	system_id = Column(Integer, ForeignKey('system.id'))
	system = relationship('System', backref=backref('file'))

	__table_args__ = (UniqueConstraint('id', 'fullpath'),)	

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

	@hybrid_property  # TODO: how to handle fullpath if change it?
	def fullpath(self):
		return self._fullpath

	@fullpath.setter
	def fullpath(self, fullpath):
		if fullpath is None:
			return 
		self._fullpath = None	
		path, filename, ext = FileUtils.split(fullpath)		
		self.path = path
		self.name = filename
		self.ext = ext	
		self._fullpath = fullpath

	def _make_fullpath(self):
		if self._fullpath is None:
			return
		elif self.ext == '':
			if self.path == '':
				return self.name
			else:
				return self.path + self.name
		elif self.path == '':
			return self.name + '.' + self.ext
		return self.path + '/' + self.name + '.' + self.ext
