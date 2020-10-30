import sys
import javalang
from javalang import parser
from .parse_exceptions import SyntaxException

class JavaParser():
	"""JavaParser"""
	def parser(self, src):
		sys.setrecursionlimit(10**6) 
		try:
			self.tree = javalang.parse.parse(src)
		except parser.JavaSyntaxError:
			raise SyntaxException('SyntaxException')

	def extract_operations(self):
		classes = []
		self._walk_to_classes(self.tree.children, classes)
		class_operations = []
		for c in classes:
			class_operations.append({'name': c.name,
								 'operations': self._extract_declarations(c),
								 'modifiers': self._get_method_modifier(c)})
		return class_operations

	def extract_calls(self):
		return self._extract_invocations() + self._extract_annotations()

	def extract_associations(self):
		return self._extract_imports()

	def _extract_imports(self):
		imports = []
		for path, node in self.tree.filter(javalang.tree.Import):
			imports.append(node.path.replace('.', '/'))		
		return imports

	def _extract_methods(self):
		methods = []
		for path, node in self.tree.filter(javalang.tree.MethodDeclaration):
			modifiers = self._get_method_modifier(node)
			methods.append({'name': node.name, 'modifiers': modifiers})
		return methods

	def _get_method_modifier(self, node):
		modifiers = {}
		for modifier in node.modifiers:
			modifiers[modifier] = modifier

		return modifiers

	def _extract_invocations(self):
		calls = []
		for path, node in self.tree.filter(javalang.tree.MethodInvocation):
			calls.append(node.member)
		return calls	

	def _extract_annotations(self):
		annotations = []
		for path, node in self.tree.filter(javalang.tree.Annotation):
			annotations.append(node.name)
		return annotations

	def _extract_declarations(self, tree):
		declarations = []
		for path, node in tree.filter(javalang.tree.Declaration):
			if (isinstance(node, javalang.tree.AnnotationDeclaration)
				or isinstance(node, javalang.tree.MethodDeclaration)
				or isinstance(node, javalang.tree.ConstructorDeclaration)):
				modifiers = self._get_method_modifier(node)
				declarations.append({'name': node.name, 'modifiers': modifiers})
		return declarations		

	def _walk_to_classes(self, children, classes):
		if isinstance(children, list):
			for child in children:
				if child:
					if isinstance(child, list):
						self._walk_to_classes(child, classes)
					elif isinstance(child, javalang.tree.Node):
						if (isinstance(child, javalang.tree.ClassDeclaration)
								or isinstance(child, javalang.tree.AnnotationDeclaration)):
							classes.append(child)
					else:
						raise NotImplementedError('Experimental exception.')
		elif isinstance(child, javalang.tree.Node):	
			raise NotImplementedError('Experimental exception.')
