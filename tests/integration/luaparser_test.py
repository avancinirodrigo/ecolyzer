from ecolyzer.parser import LuaParser

import os

def test_extract_functions():
	luafile = os.path.join(os.path.dirname(__file__), 'data', 'Utils.lua')
	src = open(luafile).read()
	parser = LuaParser()
	parser.parser(src)
	functions = parser.extract_functions()

	file_functions = {
		'clean' : True,
		'clone' : True,
		'belong' : True,
		'equals' : True,
		'isModel' : True,
		'call' : True,
		'd' : True,
		'delay' : True,
		'forEachAgent' : True,
		'forEachAttribute' : True,
		'forEachCell' : True,
		'forEachCellPair' : True,
		'forEachConnection' : True,
		'forEachElement' : True,
		'forEachFile' : True,
		'forEachDirectory' : True,
		'forEachRecursiveDirectory' : True,
		'forEachModel' : True,
		'forEachNeighbor' : True,
		'forEachNeighborAgent' : True,
		'forEachNeighborhood' : True,
		'forEachOrderedElement' : True,
		'forEachSocialNetwork' : True,
		'getConfig' : True,
		'getLuaFile' : True,
		'getn' : True,
		'getNames' : True,
		'greaterByAttribute' : True,
		'greaterByCoord' : True,
		'integrate' : True,
		'integrationEuler' : True,
		'integrationHeun' : True,
		'integrationRungeKutta' : True,
		'isTable' : True,
		'levenshtein' : True,
		'round' : True,
		'toLabel' : True,
		'switch' : True,
		'type' : True,
		'vardump' : True,
		'replaceLatinCharacters' : True
	}

	assert len(functions) == len(file_functions)

	for func in functions:
		assert file_functions[func]

