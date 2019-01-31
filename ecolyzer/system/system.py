from sqlalchemy import Column, String, Integer

from ecolyzer.dataaccess import Base

class System(Base):
	__tablename__ = 'system'

	id = Column(Integer, primary_key=True)
	name = Column(String)

	def __init__(self, name):
		self.name = name
