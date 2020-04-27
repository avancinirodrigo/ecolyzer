import javalang

src = open('../git/ecolyzer/tests/integration/data/FileSerializer.java').read()

ast = javalang.parse.parse(src)

print(ast.package.name)

#print(tree.types)

# for t in tree.types:
# 	print(t)
# 	print('')

def methods():
	for path, node in ast.filter(javalang.tree.MethodDeclaration):
		print(node.name)
		print(node.modifiers, next(iter(node.modifiers)))
		print("")
		print("")

def calls():
	for path, node in ast.filter(javalang.tree.MethodInvocation):
		print(node.member)
		#print(node.arguments)
		print(node)
		print("")
		print("")

def invoc():
	for path, node in ast.filter(javalang.tree.Invocation):
		print(node)
		print("")
		print("")		

def class_ref():
	for path, node in ast.filter(javalang.tree.ClassReference):
		print(node.type)
		print("")
		print("")		

def imports():
	for path, node in ast.filter(javalang.tree.Import):
		print(node.path)
		print("")
		print("")

#methods()
#calls()
#invoc()
#class_ref()
imports()