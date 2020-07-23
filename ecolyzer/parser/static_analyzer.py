from ecolyzer.system import Operation, Call, Association
from .lua_parser import LuaParser
from .lizard import Lizard
from .java_parser import JavaParser
from .parse_exceptions import SyntaxException, ChunkException

class StaticAnalyzer:
	def __init__(self):
		pass

	def reverse_engineering(self, src_file, src):
		if src_file.ext == 'lua':
			return self._lua_reverse_engineering(src_file, src)
		elif src_file.ext == 'java':
			return self._java_reverse_engineering(src_file, src)

	def _java_reverse_engineering(self, src_file, src):
		code_elements = []
		parser = JavaParser()
		try:
			parser.parser(src)

			methods = parser.extract_operations()
			operations = [method['name'] for method in methods]
			self._remove_methods_duplicated(methods)
			self._remove_private_modifiers(methods)
			for op in methods:
				code_elements.append(Operation(op, src_file))		

			calls = parser.extract_calls()
			self._remove_inner_calls(calls, operations)
			self._remove_duplicated(calls)		
			for call in calls:
				code_elements.append(Call(call, src_file))			

			associations = parser.extract_associations()
			for ass in associations:
				code_elements.append(Association(ass, src_file))
		except SyntaxException:
			pass

		return code_elements

	def _lua_reverse_engineering(self, src_file, src):
		code_elements = []
		parser = LuaParser()
		try:
			parser.parser(src)
			functions = (parser.extract_functions() 
						+ parser.extract_table_functions())
			self._remove_duplicated(functions)
			for func in functions:
				code_elements.append(Operation(func, src_file))

			calls = parser.extract_calls() + parser.extract_global_calls()
			local_functions = parser.extract_local_functions()
			all_functions = functions + local_functions
			self._remove_inner_calls(calls, all_functions)
			self._remove_duplicated(calls)
			for call in calls:
				code_elements.append(Call(call, src_file))
		except SyntaxException:
			pass
		except ChunkException:
			pass

		return code_elements

	def _remove_private_modifiers(self, methods):
		result = []
		for method in methods:
			if (('public' in method['modifiers']) 
					or ('protected' in method['modifiers'])):
				result.append(method['name'])	
		methods[:] = result

	def nloc(self, filepah, source_code):
		lizard = Lizard(filepah, source_code)
		return lizard.nloc()

	# def _remove_inner_methods_calls(self, calls, methods):
	# 	external_calls = []
	# 	for call in calls:
	# 		if call not in methods.values():
	# 			external_calls.append(call)

	# 	calls[:] = external_calls

	def _remove_inner_calls(self, calls, functions):
		external_calls = []
		for call in calls:
			if call not in functions:
				external_calls.append(call)

		calls[:] = external_calls

	def _remove_methods_duplicated(self, methods):
		methods_map = {}
		result = []
		for method in methods:
			if method['name'] not in methods_map:
				methods_map[method['name']] = True
				result.append(method)

		methods[:] = result		
			

	def _remove_duplicated(self, calls):
		calls_aux = {}
		result = []
		for call in calls:
			if call not in calls_aux:
				calls_aux[call] = call
				result.append(call)

		calls[:] = result

	def number_of_calls(self, source_file, source_code, code_element):
		parser = None
		if source_file.ext == 'lua':
			parser = LuaParser()
			parser.parser(source_code)
			calls = parser.extract_calls() + parser.extract_global_calls()
		elif source_file.ext == 'java':
			parser = JavaParser()
			parser.parser(source_code)
			calls = parser.extract_calls() 
		else:
			raise SourceFileNotSupportedException('Source file \'{0}\' not supported.'.\
				format(source_file.ext))
		
		return calls.count(code_element)
			
class SourceFileNotSupportedException(Exception):
	pass			