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

	def __init__(self, commit_info, repository):
		self.hash = commit_info.hash
		self.date = commit_info.date
		self.msg = commit_info.msg
		self.repository = repository
		
class CommitInfo:
	def __init__(self, hash):
		self.hash = hash
		self.date = None
		self.msg = None		

	    #'Hash: {}\n'.format(commit.hash),
        #'Author: {}'.format(commit.author.name),
        #'Committer: {}'.format(commit.committer.name),
        #'In project named: {}'.format(commit.project_name),
        #'In path: {}'.format(commit.project_path),
        #'Author date: {}'.format(commit.author_date.strftime("%Y-%m-%d %H:%M:%S")),
        #'Message: {}'.format(commit.msg),
        #'Merge: {}'.format(commit.merge),
        #'In main branch: {}'.format(commit.in_main_branch)	