from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import attribute_mapped_collection
from ecolyzer.dataaccess import Base
from .author import Author
from .repository_miner import RepositoryMiner

class Repository(Base):
	"""Repository"""
	__tablename__ = 'repository'

	id = Column(Integer, primary_key=True)
	path = Column(String, nullable=False, unique=True)
	_developers = relationship(Author, 
					collection_class=attribute_mapped_collection('email'))

	def __init__(self, path):
		if RepositoryMiner.IsGitRepo(path):
			self.path = path
		else:
			raise Exception('Invalid repository path \'{0}\''.format(path))

	def add_developer(self, author):
		if author not in self._developers: 
			self._developers[author.email] = author
		else:
			raise ValueError('Developer \'{0}\' is already present'.format(author.name))

	def developer_exists(self, email):
		return email in self._developers

	def get_developer(self, email):
		if self.developer_exists(email):
			return self._developers[email]
		else:
			raise ValueError('Developer \'{0}\' not exists'.format(email))
