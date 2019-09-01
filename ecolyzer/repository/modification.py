from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from ecolyzer.dataaccess import Base

class Modification(Base):
	"""Modification"""
	__tablename__ = 'modification'

	id = Column(Integer, primary_key=True)
	old_path = Column(String)
	new_path = Column(String)
	added = Column(Integer)
	removed = Column(Integer)
	status = Column(String, nullable=False)
	source_code = Column(String)
	commit_id = Column(Integer, ForeignKey('commit.id'))
	commit = relationship('Commit', backref=backref('modification', cascade='all,delete'))
	file_id = Column(Integer, ForeignKey('file.id'))
	file = relationship('File', backref=backref('modification'))	

	def __init__(self, mod_info, file, commit):
		self.old_path = mod_info.old_path
		self.new_path = mod_info.new_path
		self.added = mod_info.added
		self.removed = mod_info.removed
		self.status = mod_info.status
		self.source_code = mod_info.source_code		
		self.commit = commit
		self.file = file

	def author(self):
		return self.commit.author
	
class ModificationInfo:
	def __init__(self, filename):
		self.filename = filename
		self.old_path = ''
		self.new_path = ''
		self.added = 0
		self.removed = 0
		self.status = ''
		self.source_code = None
