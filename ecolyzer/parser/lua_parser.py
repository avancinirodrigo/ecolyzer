from luaparser import ast
from luaparser import astnodes

class LuaParser(object):
	_instance = None

	def __new__(cls):
		if cls._instance is None:
			cls._instance = object.__new__(cls)

		return cls._instance
		
	def parser(self, src):
		self.tree = ast.parse(src)
		
	def extract_functions(self):
		visitor = FunctionVisitor() 
		visitor.visit(self.tree)
		return visitor.functions
		
class FunctionVisitor(ast.ASTVisitor):
	functions = []
	def visit_Function(self, node):
		if isinstance(node.name, astnodes.Name):
			self.functions.append(node.name.id)
