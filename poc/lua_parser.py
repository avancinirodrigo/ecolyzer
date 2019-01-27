from luaparser import ast
from luaparser import astnodes

#src = open('repo/terrame/packages/base/lua/CellularSpace.lua').read()
#print(src)

# src = """
	# -- comment
	# function sayHello()
		# print('hello world !')
	# end
    # local say = sayHello()
	# """
	
src = """
	local function sayOla(s)
		s.msg = "Ola!"
		print(s.msg)
	end
	
	local ola = {}
	sayOla(ola)
	""" 

class NumberVisitor(ast.ASTVisitor):
	def visit_Number(self, node):
		print('Number value = ' + str(node.n))

class FunctionVisitor(ast.ASTVisitor):
	def visit_Function(self, node):
		print(node.name.id)
		for arg in node.args:
			print(arg.id)
		for block in node.body.body:
			if isinstance(block, astnodes.Call):
				print(block.func.id)
				for arg in block.args:
					if isinstance(arg, astnodes.Name):
						print(arg.id)					
					if isinstance(arg, astnodes.String):
						print(arg.s)

class TableVisitor(ast.ASTVisitor):
	def visit_Table(self, node):
		print(node)
		for field in node.fields:
			if isinstance(field.key, astnodes.Name):
				print(field.key.id)
				
class TableVisitor(ast.ASTVisitor):
	def visit_Table(self, node):
		print(node)
		for field in node.fields:
			if isinstance(field.key, astnodes.Name):
				print(field.key.id)
				
class AssignVisitor(ast.ASTVisitor):
	def visit_Assign(self, node):
		print(node)
		for target in node.targets:
			if isinstance(target, astnodes.Index):
				#print(target)
				#print(target.idx)
				if isinstance(target.idx, astnodes.Name):
					print(target.idx.id)
				if isinstance(target.value, astnodes.Name):
					print(target.value.id)
			elif isinstance(target, astnodes.Name):
				print(target.id)
						
class LabelVisitor(ast.ASTVisitor):
	def visit_Label(self, node):
		print(node)
		# for field in node.fields:
			# if isinstance(field.key, astnodes.Name):
				# print(field.key.id)
				
class MethodVisitor(ast.ASTVisitor):
	def visit_Method(self, node):
		print(node)
						
tree = ast.parse(src)
#print(tree)
#print(ast.toPrettyStr(tree))
print(ast.to_xml_str(tree))

#for node in ast.walk(tree):
	#if isinstance(node, astnodes.Name):
	#	print(node.id)
#	if isinstance(node, astnodes.Function):
#		print(node)

#NumberVisitor().visit(tree)
#FunctionVisitor().visit(tree)
#TableVisitor().visit(tree)
#AssignVisitor().visit(tree)
#LabelVisitor().visit(tree)
#MethodVisitor().visit(tree)
