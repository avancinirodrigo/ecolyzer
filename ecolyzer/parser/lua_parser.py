from luaparser import ast
from luaparser import astnodes

class LuaParser:
	def parser(self, src):
		self.tree = ast.parse(src)

	def extract_functions(self):
		visitor = FunctionVisitor()
		visitor.visit(self.tree)
		return visitor.functions

class FunctionVisitor(ast.ASTVisitor):
	def __init__(self):
		self.functions = []
		
	def visit_Function(self, node):
		if isinstance(node.name, astnodes.Name):
			self.functions.append(node.name.id)
