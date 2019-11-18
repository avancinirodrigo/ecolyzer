from ecolyzer.system import Operation, Call
from .lua_parser import LuaParser, SyntaxException, ChunkException

class StaticAnalyzer:
	def __init__(self):
		pass

	def lua_reverse_engineering(self, src_file, src):
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
			self._remove_inner_calls(calls, local_functions)
			self._remove_duplicated(calls)
			for call in calls:
				code_elements.append(Call(call, src_file))
		except SyntaxException:
			pass
		except ChunkException:
			pass

		return code_elements

	def _remove_inner_calls(self, calls, functions):
		external_calls = []
		for call in calls:
			if call not in functions:
				external_calls.append(call)

		calls[:] = external_calls

	def _remove_duplicated(self, calls):
		calls_aux = {}
		result = []
		for call in calls:
			if call not in calls_aux:
				calls_aux[call] = call
				result.append(call)

		calls[:] = result