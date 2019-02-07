from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from ecolyzer.dataaccess import Base

class FileModification(Base):
	"""FileModification"""
	__tablename__ = 'file_modification'

	id = Column(Integer, primary_key=True)
	old_path = Column(String, unique=True)
	new_path = Column(String, unique=True)
	added = Column(Integer)
	removed = Column(Integer)
	type = Column(String, nullable=False)
	commit_id = Column(Integer, ForeignKey('commit.id'))
	commit = relationship('Commit', backref=backref('file_modification'))
	file_id = Column(Integer, ForeignKey('file.id'))
	file = relationship('File', backref=backref('file_modification'))	

	def __init__(self, mod_info, file, commit):
		self.old_path = mod_info.old_path
		self.new_path = mod_info.new_path
		self.added = mod_info.added
		self.removed = mod_info.removed
		self.type = mod_info.type
		self.commit = commit
		self.file = file
	
class FileModificationInfo:
	def __init__(self, filename):
		self.filename = filename
		self.old_path = ''
		self.new_path = ''
		self.added = 0
		self.removed = 0
		self.type = ''
