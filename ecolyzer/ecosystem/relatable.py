from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from ecolyzer.dataaccess import Base

class Relatable(Base):
	"""Relatable"""
	__tablename__ = 'relatable'

	rid = Column('id', Integer, primary_key=True)
	rtype = Column('type', String)

	#__mapper_args__ = {'polymorphic_on':rtype}
	def __init__(self, type):
		self.rtype = type