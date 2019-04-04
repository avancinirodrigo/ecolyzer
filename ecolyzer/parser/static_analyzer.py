from ecolyzer.system import Operation, Call
from .lua_parser import LuaParser

class StaticAnalyzer:
	def __init__(self):
		pass

	def lua_reverse_engineering(self, src):
		code_elements = []
		parser = LuaParser()
		parser.parser(src)
		functions = (parser.extract_functions() 
					+ parser.extract_local_functions()
					+ parser.extract_table_functions())
		for func in functions:
			code_elements.append(Operation(func))

		calls = parser.extract_calls() + parser.extract_global_calls()
		self._remove_inner_calls(calls, functions)
		for call in calls:
			code_elements.append(Call(call))

		return code_elements

	def _remove_inner_calls(self, calls, functions):
		external_calls = []
		for call in calls:
			if call not in functions:
				external_calls.append(call)

		calls[:] = external_calls