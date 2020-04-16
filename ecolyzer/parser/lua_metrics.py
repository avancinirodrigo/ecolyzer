import lizard

class LuaMetrics(object):
	"""LuaMetrics"""
	def __init__(self, filepath, source_code):
		self.metrics = lizard.analyze_file.\
						analyze_source_code(filepath, source_code)

	def nloc(self):
		return self.metrics.nloc