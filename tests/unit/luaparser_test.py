from ecolyzer.parser import LuaParser

def test_extract_globals():
	src = """
			v1 = "global"
			local v2 = "local"
			f1 = function() end
			local f2 = function() end
			v3 = {}
			v3.f3 = function() end
		"""
	parser = LuaParser()
	parser.parser(src)
	globals = parser.extract_globals()

	assert len(globals) == 4
	assert globals[0] == 'v1'
	assert globals[1] == 'f1'
	assert globals[2] == 'v3'
	assert globals[3] == 'v3.f3'
