from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import attribute_mapped_collection
from ecolyzer.dataaccess import Base
from ecolyzer.utils import FileUtils
from .author import Author
from .commit import Commit
from .gitpython import GitPython

class Repository(Base):
	"""Repository"""
	__tablename__ = 'repository'

	id = Column(Integer, primary_key=True)
	_path = Column('path', String, nullable=False, unique=True)
	_authors = relationship(Author, 
					collection_class=attribute_mapped_collection('email'))
	_commits = relationship(Commit, 
					collection_class=attribute_mapped_collection('hash'))

	def __init__(self, path):
		if GitPython.IsGitRepo(path):
			self._path = path
		else:
			raise Exception('Invalid repository path \'{0}\''.format(path))

	@property
	def path(self):
		return self._path

	@path.setter
	def path(self, path):
		self._path = path		

	def add_author(self, author):
		if author.email not in self._authors: 
			self._authors[author.email] = author
			author.repository = self
		else:
			raise ValueError('Author \'{0}\' is already present'.format(author.name))

	def author_exists(self, email):
		return email in self._authors

	def get_author(self, email):
		if self.author_exists(email):
			return self._authors[email]
		else:
			raise ValueError('Author \'{0}\' not exists'.format(email))

	def add_commit(self, commit):
		if not self.commit_exists(commit.hash): 
			self._commits[commit.hash] = commit
		else:
			raise ValueError('Commit \'{0}\' is already present'.format(commit.hash))

	def commit_exists(self, hash):
		return hash in self._commits

	def get_commit(self, hash):
		if self.commit_exists(hash):
			return self._commits[hash]
		else:
			raise ValueError('Commit \'{0}\' not exists'.format(hash))

	@property
	def name(self) -> str:
		return FileUtils.last_dir(self._path)
	
