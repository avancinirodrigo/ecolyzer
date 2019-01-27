from luaparser import ast
from luaparser import astnodes

class LuaParser(object):
	_instance = None

	def __new__(cls):
		if cls._instance is None:
			cls._instance = object.__new__(cls)

		return cls._instance
		
	def parser(self, source_code):
		
		
	def extract_function(self, source_code):
		