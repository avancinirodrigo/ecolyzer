import javalang

class JavaParser():
	"""JavaParser"""
	def parser(self, src):
		self.tree = javalang.parse.parse(src)

	def extract_operations(self):
		return self._extract_methods()

	def extract_calls(self):
		return self._extract_invocations()

	def extract_associations(self):
		return self._extract_imports()

	def _extract_imports(self):
		imports = []
		for path, node in self.tree.filter(javalang.tree.Import):
			imports.append(node.path)		
		return imports

	def _extract_methods(self):
		methods = []
		for path, node in self.tree.filter(javalang.tree.MethodDeclaration):
			modifier = self._get_method_modifier(node)
			methods.append(node.name)
		return methods

	def _get_method_modifier(self, node):
		return next(iter(node.modifiers))

	def _extract_invocations(self):
		calls = []
		for path, node in self.tree.filter(javalang.tree.MethodInvocation):
			calls.append(node.member)
		return calls	 
