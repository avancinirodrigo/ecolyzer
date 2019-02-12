from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from ecolyzer.dataaccess import Base

class Commit(Base):
	"""Commit"""
	__tablename__ = 'commit'

	id = Column(Integer, primary_key=True)
	hash = Column(String, nullable=False, unique=True)
	date = Column(DateTime, nullable=False)
	msg = Column(String)
	repo_id = Column(Integer, ForeignKey('repository.id'))
	repository = relationship('Repository', backref=backref('commit', cascade='all,delete'))
	author_id = Column(Integer, ForeignKey('author.id'))
	author = relationship('Author', backref=backref('commit'))

	def __init__(self, commit_info, author, repository):
		self.hash = commit_info.hash
		self.date = commit_info.date.replace(tzinfo=None)
		self.msg = commit_info.msg
		self.author = author
		self.repository = repository

class CommitInfo:
	def __init__(self, hash):
		self.hash = hash
		self.date = None
		self.msg = None
		self.author_name = None
		self.author_email = None
		self.modifications = None
