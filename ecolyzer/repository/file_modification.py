from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from ecolyzer.dataaccess import Base

class FileModification(Base):
	"""FileModification"""
	__tablename__ = 'file_modification'

	id = Column(Integer, primary_key=True)
	old_path = Column(String, nullable=False, unique=True)
	new_path = Column(String, nullable=False, unique=True)
	added = Column(Integer)
	# date = Column(DateTime, nullable=False)
	# msg = Column(String)
	# repo_id = Column(Integer, ForeignKey('repository.id'))
	# repository = relationship('Repository', backref=backref('commit', cascade='all,delete'))
	commit_id = Column(Integer, ForeignKey('commit.id'))
	commit = relationship('Commit', backref=backref('file_modification'))

	def __init__(self, mod_info, commit):
		self.filename = mod_info.filename
		self.old_path = mod_info.old_path
		self.new_path = mod_info.new_path
		self.added = mod_info.added
		self.commit = commit
	
class FileModificationInfo:
	def __init__(self, filename):
		self.filename = filename
		self.old_path = None
		self.new_path = None
		self.added = 0
		self.removed = 0
