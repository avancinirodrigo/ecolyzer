from luaparser import ast
from luaparser import astnodes

src = open('repo/terrame/packages/base/lua/CellularSpace.lua').read()
#print(src)

# src = """
	# -- comment
	# function sayHello()
		# print('hello world !')
	# end
    # local say = sayHello()
	# """
	
# src = """
# 	local function sayOla(s)
# 		s.msg = "Ola!"
# 		print(s.msg)
# 	end
	
# 	local ola = {}
# 	sayOla(ola)
# 	""" 

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

class LocalFunctionVisitor(ast.ASTVisitor):
	def visit_LocalFunction(self, node):
		#print(node.__dict__)
		print(node.name.id)

class TableVisitor(ast.ASTVisitor):
	def visit_Table(self, node):
		#('---', node.__dict__)
		for field in node.fields:
			print(field.__dict__)
		#	if isinstance(field.key, astnodes.Name):
		#		print(field.key.id)
				
class AssignVisitor(ast.ASTVisitor):
	def visit_Assign(self, node):
		#print(node.__dict__)
		# print('--')
		# for target in node.targets:
		# 	#print(target.__dict__)
		# 	if isinstance(target, astnodes.Name):
		# 		#print(target.id) #__dict__)
		# 		print()
		# 	elif isinstance(target, astnodes.Index):
		# 		#print()
		# 		#print(target.idx.__dict__)
		# 		# print(target.value.__dict__)
		# 		if isinstance(target.value, astnodes.Index):
		# 			print(target.value.value.__dict__)
		# # 		#print(target.idx)
		# 		print()
		# # 		if isinstance(target.idx, astnodes.Name):
		# # 			print(target.idx.id)
		# # 		if isinstance(target.value, astnodes.Name):
		# # 			print(target.value.id)
		# # 	elif isinstance(target, astnodes.Name):
		# # 		print(target.id)
			#else:
				#print(target.__dict__)
		for value in node.values:
			print(value.__dict__)
						
class LabelVisitor(ast.ASTVisitor):
	def visit_Label(self, node):
		print(node)
		# for field in node.fields:
			# if isinstance(field.key, astnodes.Name):
				# print(field.key.id)
				
class MethodVisitor(ast.ASTVisitor):
	def visit_Method(self, node):
		print(node)

class CallVisitor(ast.ASTVisitor):
	def visit_Call(self, node):
		#print(node.func.__dict__)
		if isinstance(node.func, astnodes.Name):
			#print(node.func.__dict__)
			print('Name->', node.func.id)
		elif isinstance(node.func, astnodes.Index):
			print()
		# 	#print(node.func.__dict__)
		# 	if isinstance(node.func.idx, astnodes.String):
		# 		print('Index.String----->', node.func.idx.s) #__dict__)
		# 	elif isinstance(node.func.idx, astnodes.Name):
		# 		print('Index.Name----->', node.func.idx.__dict__)
		# 	#else: 
				#print(node.func.idx.__dict__)
		else:
			print(node.func)
			#self.visit_Call(node.func)

class InvokeVisitor(ast.ASTVisitor):
	def visit_Invoke(self, node):
		#print(node.__dict__)
		if (isinstance(node.func, astnodes.Name) 
				and isinstance(node.source, astnodes.Name)):
			#print(node.source.id, node.func.id)
			print()

		elif isinstance(node.func, astnodes.Name):
				print(node.func.id) #, node.source.__dict__) #, node.source.idx.__dict__)
				if isinstance(node.source, astnodes.Index):
					if isinstance(node.source.idx, astnodes.String): 
						if isinstance(node.source.value, astnodes.Name):
							print(node.source.idx.s, node.source.value.id)
				#	print(node.func.id, node.source.idx.s)
				#if isinstance(node.source, astnodes.Index):
				#	print()
		else:
			print(node.func.__dict__)
		#	print(node.__dict__)
		# 	print('Func.Name----->', node.func.id) #__dict__)
		# 	if isinstance(node.source, astnodes.Index):
		# 		if isinstance(node.source.idx, astnodes.String):
		# 			print('Source.Index.String-->', node.source.idx.s)
		# 	# if isinstance(node.source, astnodes.String):
		# 	# 	print('Source.String--->', node.source.idx.s) #__dict__)
		# 	elif isinstance(node.source, astnodes.Call):
		# 		print('Source.Call.Function', node.source.func.id) # __dict__)
		# 	else:
		# 		print('-----', node.source)	
						
tree = ast.parse(src)

# for node in ast.walk(tree):
# 	print(node._name) #__dict__)
	# if isinstance(node, astnodes.Assign): 
	# 	#print(node.__dict__)
 # 		for target in node.targets:
 # 			if isinstance(target, astnodes.Index):
 # 				print(target.value.id, target.idx.s)
 # 			elif isinstance(target, astnodes.Name):
 # 				print(target.id) #__dict__)
 # 			else:
 # 				print('target', target.__dict__)
 # 		for value in node.values:
 # 			if isinstance(value, astnodes.String):
 # 				print(value.s)
 # 			else:
 # 				print('value', value)

#print(tree)
#print(ast.toPrettyStr(tree))
#print(ast.to_xml_str(tree))

#print(tree.body.__dict__)
# for node in tree.body.body:
#  	if (isinstance(node, astnodes.Assign) 
#  			and not isinstance(node, astnodes.LocalAssign)):	
#  		print('--------------------------')
#  		for target in node.targets:
#  			if isinstance(target, astnodes.Index):
#  				print(target.value.id, target.idx.s)
#  			elif isinstance(target, astnodes.Name):
#  				print(target.id) #__dict__)
#  			else:
#  				print('target', target.__dict__)
#  		for value in node.values:
#  			if isinstance(value, astnodes.String):
#  				print(value.s)
#  			else:
#  				print('value', value)
 		#print(node.values.__dict__)
# 		print()
 	# elif isinstance(node, astnodes.Call):
 	# 	print(node.func.__dict__)
 	# else:
 	# 	print(node) #.__dict__)

#for node in ast.walk(tree):
	#print(node)a
#	if isinstance(node, astnodes.Assign):
#		print(node)
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
#CallVisitor().visit(tree)
#InvokeVisitor().visit(tree)
LocalFunctionVisitor().visit(tree)