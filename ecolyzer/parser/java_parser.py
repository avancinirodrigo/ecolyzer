import sys
import traceback
import javalang
from javalang import parser
from javalang import tokenizer
from .parse_exceptions import SyntaxException, LexerException

class JavaParser():
	"""JavaParser"""
	def parser(self, src):
		sys.setrecursionlimit(10**6) 
		try:
			self.tree = javalang.parse.parse(src)
		except parser.JavaSyntaxError:
			raise SyntaxException('SyntaxException')
		except tokenizer.LexerError:
			raise LexerException('LexerException')
		except Exception as e:
			print(e)
			traceback.print_exc()
			raise e

	def extract_operations(self):
		classes = []
		self._walk_to_classes(self.tree.children, classes)
		class_operations = []
		for clas in classes:
			operations = self._inheritance_operations(clas)\
						+ self._extract_declarations(clas)
			class_operations.append({'name': clas.name,
								 'operations': operations,
								 'modifiers': self._get_modifier(clas)})
		return class_operations

	def extract_calls(self):
		classes = []
		self._walk_to_classes(self.tree.children, classes)						
		return (self._extract_invocations(classes) 
				+ self._extract_annotations()
				+ self._extract_inheritance(classes))

	def extract_associations(self):
		return self._extract_imports()

	def _extract_imports(self):
		imports = []
		for path, node in self.tree.filter(javalang.tree.Import):
			imports.append(node.path.replace('.', '/'))		
		return imports

	def _get_modifier(self, node):
		modifiers = {}
		for modifier in node.modifiers:
			modifiers[modifier] = modifier
		return modifiers

	def _extract_invocations(self, classes):
		class_vars = {}
		declarations = []
		initializers = []

		for clas in classes:
			if isinstance(clas, javalang.tree.ClassDeclaration):
				self._set_declarations(clas, clas.body, declarations, initializers,
										class_vars, classes)
			elif isinstance(clas, javalang.tree.EnumDeclaration):
				self._set_declarations(clas, clas.body.declarations, declarations, 
									initializers, class_vars, classes)

		calls = []		
		for decl in declarations:
			method_vars = class_vars.copy()
			if isinstance(decl['declaration'], list):
				for d in decl['declaration']:
					self._add_declaration(d, decl, calls, method_vars)
			else:
				self._add_parameters(method_vars, decl['declaration'])
				if not isinstance(decl['declaration'], 
							javalang.tree.AnnotationDeclaration):
					self._add_throws(calls, decl['declaration'])
				if not self._is_method_abstract(decl['declaration']):
					for elem in decl['declaration'].body:
						self._add_declaration(elem, decl, calls, method_vars)

		for init in initializers:
			self._add_declaration(init['initializer'], init, calls, class_vars)

		return calls

	def _set_declarations(self, clas, body, declarations, initializers, class_vars, classes):
		for elem in body:
			if isinstance(elem, javalang.tree.FieldDeclaration):
				class_vars[elem.declarators[0].name] = elem.type.name
				if elem.declarators[0].initializer:
					initializers.append({'initializer': elem.declarators[0].initializer,
										'class': clas})
			elif (isinstance(elem, javalang.tree.ClassDeclaration) 
					or isinstance(elem, javalang.tree.EnumDeclaration)
					or isinstance(elem, javalang.tree.InterfaceDeclaration)):
				classes.append(elem)			
			else:
				declarations.append({'declaration': elem, 'class': clas})		

	def _is_method_abstract(self, method):
		return method.body == None

	def _add_throws(self, calls, decl):
		if decl.throws:
			for throw in decl.throws:
				calls.append({'ref': f'{throw}.{throw}', 'caller': 'throws'})

	def _add_declaration(self, elem, decl, calls, method_vars):
		if isinstance(elem, javalang.tree.StatementExpression):
			self._add_declaration(elem.expression, decl, calls, method_vars)
		elif isinstance(elem, javalang.tree.MethodInvocation):
			self._process_method_invocation(elem, decl, calls, method_vars)
		elif isinstance(elem, javalang.tree.Assignment):
			self._process_assignment(elem, decl, calls, method_vars)
		elif isinstance(elem, javalang.tree.BinaryOperation):
			self._binary_operation(elem, decl, calls, method_vars)
		elif isinstance(elem, javalang.tree.VariableDeclaration):
			self._process_variable_declaration(elem, decl, calls, method_vars)
		elif isinstance(elem, javalang.tree.ReturnStatement):
			self._add_declaration(elem.expression, decl, calls, method_vars)
		elif isinstance(elem, javalang.tree.TryStatement): 
			self._process_try_statement(elem, decl, calls, method_vars)
		elif isinstance(elem, javalang.tree.ForStatement): 
			self._process_for_statement(elem, decl, calls, method_vars)
		elif isinstance(elem, javalang.tree.IfStatement): 
			self._process_if_statement(elem, decl, calls, method_vars)
		elif isinstance(elem, javalang.tree.This): 
			self._process_this(elem, decl, calls, method_vars)
		elif isinstance(elem, javalang.tree.SwitchStatement): 
			self._process_switch(elem, decl, calls, method_vars)
		elif isinstance(elem, javalang.tree.ThrowStatement): 		
			self._add_declaration(elem.expression, decl, calls, method_vars)		
		elif (isinstance(elem, javalang.tree.ClassCreator)
				or isinstance(elem, javalang.tree.InnerClassCreator)):
			self._process_class_creator(elem, decl, calls, method_vars)
		elif isinstance(elem, javalang.tree.SuperConstructorInvocation):
			self._process_super_constructor_invocation(elem, decl, calls, method_vars)
		elif isinstance(elem, javalang.tree.MemberReference):
			self._process_member_reference(elem, calls, method_vars)
		elif isinstance(elem, javalang.tree.TernaryExpression):
			self._process_ternary_expression(elem, decl, calls, method_vars)
		elif isinstance(elem, javalang.tree.Cast): 
			self._process_cast(elem, decl, calls, method_vars)
		elif isinstance(elem, javalang.tree.SuperMethodInvocation): 
			self._process_super_method_invocation(elem, decl, calls, method_vars)	
		elif isinstance(elem, javalang.tree.ExplicitConstructorInvocation)	:
			self._process_explicit_constructor_invocation(elem, decl, calls, method_vars)		
		# else:
		# 	print('  --INVOCATIONS--  ', elem)	

	def _process_member_reference(self, node, calls, method_vars):
		if node.qualifier == node.member:
			return
		typeof = node.qualifier 
		if node.qualifier in method_vars:
			typeof = method_vars[node.qualifier]
			calls.append({'ref': f'{typeof}.{node.member}', 'caller': node.qualifier})
		elif typeof:
			calls.append({'ref': f'{typeof}.{node.member}', 'caller': typeof})		

	def _process_super_method_invocation(self, node, decl, calls, method_vars):
		self._add_reference(node, decl['class'], calls, method_vars)

	def _process_cast(self, node, decl, calls, method_vars):
		self._add_declaration(node.expression, decl, calls, method_vars)

	def _process_super_constructor_invocation(self, node, decl, calls, method_vars):
		if decl['class'].extends: # avoiding super Object, maybe a exception here
			parent = decl['class'].extends.name
			calls.append({'ref': f'{parent}.{parent}', 'caller': 'super'})

	def _process_class_creator(self, node, decl, calls, method_vars):
		classname = node.type.name
		calls.append({'ref': f'{classname}.{classname}', 'caller': 'new'})
		if node.type.sub_type:
			sub_type = node.type.sub_type
			calls.append({'ref': f'{classname}.{sub_type.name}', 'caller': classname})
		for arg in node.arguments:
			self._add_declaration(arg, decl, calls, method_vars)	

	def _process_if_statement(self, node, decl, calls, method_vars):
		if isinstance(node.condition, javalang.tree.BinaryOperation):
			self._binary_operation(node.condition, decl, calls, method_vars)
		else:
			self._add_declaration(node.condition, decl, calls, method_vars)
		if hasattr(node.then_statement, 'statements'):
			for stat in node.then_statement.statements:
				self._add_declaration(stat, decl, calls, method_vars)
		else:
			self._add_declaration(node.then_statement, decl, calls, method_vars)
		if node.else_statement and hasattr(node.else_statement, 'statements'):
			for stat in node.else_statement.statements:
				self._add_declaration(stat, decl, calls, method_vars)				
		else:
			self._add_declaration(node.else_statement, decl, calls, method_vars)	

	def _process_for_statement(self, node, decl, calls, method_vars):
		control = node.control
		if isinstance(control, javalang.tree.EnhancedForControl):
			self._add_declaration(control.var, decl, calls, method_vars)
			self._add_declaration(control.iterable, decl, calls, method_vars)
		else: # javalang.tree.ForControl
			self._add_declaration(control.init, decl, calls, method_vars)
			self._add_declaration(control.condition, decl, calls, method_vars)
			self._add_declaration(control.update, decl, calls, method_vars)

		if hasattr(node.body, 'statements'):
			for stat in node.body.statements:
				self._add_declaration(stat, decl, calls, method_vars)	
		else:
			self._add_declaration(node.body, decl, calls, method_vars)

	def _process_try_statement(self, node, decl, calls, method_vars):
		for d in node.block:
			self._add_declaration(d, decl, calls, method_vars)	
		if node.catches:
			for catch in node.catches:
				for d in catch.block:
					self._add_declaration(d, decl, calls, method_vars)						

	def _process_variable_declaration(self, node, decl, calls, method_vars):
		method_vars[node.declarators[0].name] = node.type.name
		initializer = node.declarators[0].initializer
		self._add_declaration(initializer, decl, calls, method_vars)

	def _process_assignment(self, node, decl, calls, method_vars):			
		self._add_declaration(node.value, decl, calls, method_vars)

	def _process_explicit_constructor_invocation(self, node, decl, calls, method_vars):	
		for arg in node.arguments:		
			self._add_declaration(arg, decl, calls, method_vars)			

	def _process_method_invocation(self, method_node, decl, calls, method_vars):
		self._add_reference(method_node, decl['class'], calls, method_vars)
		for arg in method_node.arguments:	
			self._add_declaration(arg, decl, calls, method_vars)		

	def _process_switch(self, switch_node, decl, calls, method_vars):
		for case in switch_node.cases:
			for stat in case.statements:
				self._add_declaration(stat, decl, calls, method_vars)

	def _process_ternary_expression(self, ternary_node, decl, calls, method_vars):
		self._add_declaration(ternary_node.condition, decl, calls, method_vars)
		self._add_declaration(ternary_node.if_false, decl, calls, method_vars)
		self._add_declaration(ternary_node.if_true, decl, calls, method_vars)		

	def _process_this(self, this_node, decl, calls, method_vars):
		for sel in this_node.selectors:
			if not isinstance(sel, javalang.tree.InnerClassCreator):
				qualifier = this_node.selectors[0].member
				sel.qualifier = qualifier
				if f'this.{qualifier}' in method_vars:
					local_qualifier = method_vars[qualifier]
					method_vars[qualifier] = method_vars[f'this.{qualifier}']		
					self._add_declaration(sel, decl, calls, method_vars)	
					method_vars[qualifier] = local_qualifier
				else:
					self._add_declaration(sel, decl, calls, method_vars)

	def _add_parameters(self, method_vars, declaration):
		if hasattr(declaration, 'parameters'):
			for param in declaration.parameters:
				if param.name in method_vars:
					if param.type.name != method_vars[param.name]:
						method_vars[f'this.{param.name}'] = method_vars[param.name]
				method_vars[param.name] = param.type.name

	def _binary_operation(self, node, decl, calls, method_vars):
		if not isinstance(node, javalang.tree.BinaryOperation):
			self._add_declaration(node, decl, calls, method_vars)
			return
		self._binary_operation(node.operandl, decl, calls, method_vars)
		self._binary_operation(node.operandr, decl, calls, method_vars)

	def _add_reference(self, node, clas, calls, method_vars):
		if (hasattr(node, 'member')
				and not isinstance(node, javalang.tree.MemberReference)): 
			typeof = node.qualifier
			caller = node.qualifier
			member = node.member
			if isinstance(node, javalang.tree.SuperMethodInvocation):
				typeof = 'Object'
				caller = 'super'
				if not isinstance(clas, javalang.tree.EnumDeclaration):
					if clas.extends:
						typeof = clas.extends.name	
			else:			
				if node.qualifier in method_vars:
					typeof = method_vars[node.qualifier]
			if typeof:
				if '.' in typeof: #https://github.com/c2nes/javalang/issues/89
					caller_const = typeof.split('.')
					typeof = caller_const[0]
					caller = caller_const[1]
					if caller in method_vars:
						typeof = method_vars[caller]
					else:
						member = caller_const[1]
						caller = typeof		
				typeof = f'{typeof}.'
			else:
				typeof = f'{clas.name}.'
			calls.append({'ref': f'{typeof}{member}', 'caller': caller})	

	def _extract_annotations(self):
		annotations = []
		for path, node in self.tree.filter(javalang.tree.Annotation):
			annotations.append({'ref': f'{node.name}.@', 'caller': '@'})
		return annotations

	def _extract_inheritance(self, classes):
		inheritances = []
		for clas in classes:
			if not isinstance(clas, javalang.tree.AnnotationDeclaration):
				if not isinstance(clas, javalang.tree.EnumDeclaration):
					if clas.extends:
						exds = clas.extends
						if isinstance(exds, list):
							for e in exds:
								inheritances.append({'ref': f'extends.{e.name}', 'caller': 'extends'})
						else:
							inheritances.append({'ref': f'extends.{exds.name}', 'caller': 'extends'})
				if not isinstance(clas, javalang.tree.InterfaceDeclaration):
					if clas.implements:
						for impts in clas.implements:	
							inheritances.append({'ref': f'implements.{impts.name}', 'caller': 'implements'})	
		return inheritances

	def _extract_declarations(self, clas):
		declarations = []
		has_constructor = False
		for path, node in clas.filter(javalang.tree.Declaration):
			if isinstance(node, javalang.tree.MethodDeclaration):
				modifiers = {}
				if not isinstance(clas, javalang.tree.InterfaceDeclaration):
					modifiers = self._get_modifier(node) 
				else:
					modifiers = {'public': 'public'}
				declarations.append({'name': f'{clas.name}.{node.name}', 
									'modifiers': modifiers})
			elif isinstance(node, javalang.tree.ConstructorDeclaration):
				has_constructor = True
				modifiers = self._get_modifier(node)
				declarations.append({'name': f'{node.name}.{node.name}', 'modifiers': modifiers})
			elif isinstance(node, javalang.tree.AnnotationDeclaration):
				has_constructor = True
				modifiers = self._get_modifier(node)
				declarations.append({'name': f'{node.name}.@', 'modifiers': modifiers})				
			elif isinstance(node, javalang.tree.EnumDeclaration):
				modifiers = self._get_modifier(node)
				declarations.append({'name': node.name, 'modifiers': modifiers})
				for path, const in node.filter(javalang.tree.EnumConstantDeclaration):
					mods = {'public': 'public'}
					enum_name = node.name
					if clas.name != node.name:
						enum_name = f'{clas.name}.{node.name}'
					declarations.append({'name': f'{enum_name}.{const.name}', 
									'modifiers': mods})		
			elif isinstance(node, javalang.tree.FieldDeclaration):
				name = node.declarators[0].name	
				modifiers = self._get_modifier(node)
				declarations.append({'name': f'{clas.name}.{name}', 'modifiers': modifiers})
	
		if not has_constructor and (not isinstance(clas, 
				javalang.tree.InterfaceDeclaration)):
			declarations.append(self._default_constructor(clas))	
		return declarations

	def _inheritance_operations(self, clas):
		operations = []
		if isinstance(clas, javalang.tree.AnnotationDeclaration):
			return operations
		if isinstance(clas, javalang.tree.InterfaceDeclaration):
			operations.append({'name': f'implements.{clas.name}',
							'modifiers': {'public': 'public'}})
		elif 'final' not in clas.modifiers:
			operations.append({'name': f'extends.{clas.name}',
							'modifiers': {'public': 'public'}})
		return operations

	def _default_constructor(self, clas):
		return {'name': f'{clas.name}.{clas.name}', 'modifiers': {'public': 'public'}}

	def _walk_to_classes(self, children, classes):
		if isinstance(children, list):
			for child in children:
				if child:
					if isinstance(child, list):
						self._walk_to_classes(child, classes)
					elif isinstance(child, javalang.tree.Node):
						if isinstance(child, javalang.tree.TypeDeclaration):
							classes.append(child)
					else:
						raise NotImplementedError('Experimental exception.')
		elif isinstance(child, javalang.tree.Node):	
			raise NotImplementedError('Experimental exception.')
