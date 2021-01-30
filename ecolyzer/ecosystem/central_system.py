from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from ecolyzer.dataaccess import Base


class CentralSystem(Base):
	"""CentralSystem"""
	__tablename__ = 'central_system'

	id = Column(Integer, primary_key=True)
	system_id = Column(Integer, ForeignKey('system.id'))
	system = relationship('System', backref=backref('system', uselist=False))

	def __init__(self, system):
		self.system = system
