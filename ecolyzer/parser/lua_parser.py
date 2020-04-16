from luaparser import ast
from luaparser import astnodes
from luaparser import builder

class LuaParser:
	def parser(self, src):
		try:
			self.tree = ast.parse(src)
		except builder.SyntaxException:
			raise SyntaxException('SyntaxException')
		except Exception as e:
			if str(e) == 'Expecting a chunk':
				print("TODO: ChunkException: {0}".format(e))
				raise ChunkException(e)
			else:
				raise e

	def extract_functions(self):
		visitor = FunctionVisitor()
		visitor.visit(self.tree)
		return visitor.functions

	def extract_globals(self):
		globals = []
		for node in self.tree.body.body:
		 	if (isinstance(node, astnodes.Assign) 
		 			and not isinstance(node, astnodes.LocalAssign)):	
		 		for target in node.targets:
		 			if isinstance(target, astnodes.Index):
		 				globals.append(target.value.id + '.' + target.idx.s)
		 			elif isinstance(target, astnodes.Name):
		 				globals.append(target.id)
		 			else:
		 				raise Exception('Target not mapped\n', target.__dict__)
		return globals

	def extract_global_calls(self):
		visitor = CallVisitor()
		visitor.visit(self.tree)
		return visitor.globals

	def extract_calls(self):
		visitor = InvokeVisitor()
		visitor.visit(self.tree)
		return visitor.calls

	def extract_local_functions(self):
		visitor = LocalFunctionVisitor()
		visitor.visit(self.tree)
		return visitor.functions				

	def extract_table_functions(self):
		visitor = TableVisitor()
		visitor.visit(self.tree)
		return visitor.functions

class FunctionVisitor(ast.ASTVisitor):
	def __init__(self):
		self.functions = []
		
	def visit_Function(self, node):
		if isinstance(node.name, astnodes.Name):
			self.functions.append(node.name.id)

class CallVisitor(ast.ASTVisitor):
	def __init__(self):
		self.globals = []

	def visit_Call(self, node):
		if isinstance(node.func, astnodes.Name):
			self.globals.append(node.func.id)

class InvokeVisitor(ast.ASTVisitor):
	def __init__(self):
		self.calls = []

	def visit_Invoke(self, node):
		if isinstance(node.func, astnodes.Name):
			self.calls.append(node.func.id)

class LocalFunctionVisitor(ast.ASTVisitor):
	def __init__(self):
		self.functions = []

	def visit_LocalFunction(self, node):
		self.functions.append(node.name.id)
		
class TableVisitor(ast.ASTVisitor):
	def __init__(self):
		self.functions = []

	def visit_Table(self, node):
		for field in node.fields:
			if (isinstance(field.key, astnodes.Name) and
					isinstance(field.value, astnodes.AnonymousFunction)):
				self.functions.append(field.key.id)

class SyntaxException(Exception):
	pass

class ChunkException(Exception):
	pass
