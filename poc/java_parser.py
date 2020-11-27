import javalang

#src = open('../git/ecolyzer/tests/integration/data/JFreeChartWithInfo.java').read()
# src = """
# package org.cbsoft.framework;

# public class FileSerializer implements Serializer
# {
# 	private PostProcessor pp;

# 	public FileSerializer(PostProcessor pp)
# 	{
# 		this.pp = pp.clone();
# 	}
# }
# """		

src = """
	package net.sf.esfinge.metadata.annotation.container;

	import java.lang.annotation.Annotation;
	import java.lang.annotation.Retention;
	import java.lang.annotation.RetentionPolicy;

	import net.sf.esfinge.metadata.annotation.finder.SearchOnEnclosingElements;
	import net.sf.esfinge.metadata.container.reading.MethodProcessorsReadingProcessor;

	@Retention(RetentionPolicy.RUNTIME)
	@AnnotationReadingConfig(MethodProcessorsReadingProcessor.class)
	@SearchOnEnclosingElements

	public @interface ProcessorPerMethod {
		Class<? extends Annotation> configAnnotation();
		ProcessorType type() default ProcessorType.READER_ADDS_METADATA;

	}
"""

ast = javalang.parse.parse(src)

print(ast.package.name)

#print(tree.types)

# for t in tree.types:
# 	print(t)
# 	print('')

def methods(tree):
	for path, node in tree.filter(javalang.tree.MethodDeclaration):
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

def walk(children, level, parent):
	s = '    '*level
	print('\n', s, 'level:', level, type(children), type(parent))
	level += 1
	if level >= 3:
		return
	# for path, node in ast:
	# 	#print(node)
	# 	print(path)
	# 	print("\n")
	# def child_list(child):
	# 	for c in child.children:
	# 		if isinstance(c, list):
	# 			child_list(c)	
	# 		#print(c)
	
	# for path, node in ast:
	# 	for child in node.children:
	# 		if isinstance(child, list):
	# 			#print(child.__dict__)
	# 			#child_list(child)
	# 			#recusively do it
	# 			#for c in child.children:
	# 			#     if isinstance(child, list):	
	# 			print(child)
	#node = tree
	#print(ast.children)
	# while node:
	# 	#print(node)
	# 	if isinstance(node, list):
	# 		print('list')
	# 		for n in node:
	# 			print(type(n))
	# 		node = None
	# 	else:	
	# 		node = node.children
	if isinstance(children, list):
		print(s, '------------', 'LIST')
		count = 0
		for child in children:
			if child:
				print(s, 'i:', count, type(child))
				count += 1
		count = 0
		for child in children:
			if child:
				#print(s, '  i:', count, type(child))
				if isinstance(child, list):
					#print(s, count, '  #######', 'LIST')
					#print(s, '    ', type(child))
					walk(child, level, children)
				elif isinstance(child, javalang.tree.Node):
					print(s, count, '  #######', 'NODE')
					print(s, '    ', type(child))
					if (isinstance(child, javalang.tree.TypeDeclaration)
						or isinstance(child, javalang.tree.AnnotationDeclaration)):
						methods(child)
						print(child.name)
						print(child.modifiers)
					# walk(child.children, level, child)
				else:
					print(s, count, '  #######', 'ELSE')
					print(s, '    ', child)
				count += 1
	elif isinstance(child, javalang.tree.Node):	
		print(s, '------------', 'NODE')
		#print(s, children)
		walk(children.children, level)
		


#methods()
#calls()
#invoc()
#class_ref()
#imports()
walk(ast.children, 0, ast)