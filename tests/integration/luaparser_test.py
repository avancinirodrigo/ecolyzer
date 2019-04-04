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

	luafile = os.path.join(os.path.dirname(__file__), 'data', 'CellularSpace1.lua')
	src = open(luafile).read()
	parser = LuaParser()
	parser.parser(src)
	functions = parser.extract_functions()
	assert len(functions) == 1	
	assert functions[0] == 'CellularSpace'

def test_extract_global_calls():
	file_globals = {
		'forEachCell' : True,
		'Neighborhood' : True,
		'ipairs' : True,
		'weightF' : True,
		'filterF' : True,
		'customWarningMsg' : True,
		'namedParametersErrorMsg' : True,
		'type' : True,
		'defaultValueWarningMsg' : True,
		'incompatibleTypesErrorMsg' : True,
		'checkUnnecessaryParameters' : True,
		'mandatoryArgumentErrorMsg' : True,
		'createNeighborhood' : True,
		'createMooreNeighborhood' : True,
		'incompatibleValuesErrorMsg' : True,
		'spatialCoupling' : True,
		'createMxNNeighborhood' : True,
		'createVonNeumannNeighborhood' : True,
		'coordCoupling' : True,
		'switch' : True,
		'deprecatedFunctionWarningMsg' : True,
		'Coord' : True,
		'readCSV' : True,
		'tostring' : True,
		'Cell' : True,
		'customErrorMsg' : True,
		'load' : True,
		'pairs' : True,
		'tableParameterErrorMsg' : True,
		'resourceNotFoundErrorMsg' : True,
		'print' : True,
		'argument' : True,
		'Trajectory' : True,
		'getn' : True,
		'TeCellularSpace' : True,
		'incompatibleFileExtensionErrorMsg' : True,
		'setmetatable' : True,
		'forEachElement' : True
	}	

	luafile = os.path.join(os.path.dirname(__file__), 'data', 'CellularSpace1.lua')
	src = open(luafile).read()
	parser = LuaParser()
	parser.parser(src)
	globals = parser.extract_global_calls()

	for call in globals:
		assert file_globals[call]

def test_extract_calls():
	file_calls = {
		'get' : True,
		'add' : True,
		'addNeighborhood' : True,
		'addCell' : True,
		'getNeighborhood' : True,
		'caseof' : True,
		'getCellByID' : True,
		'getCell' : True,
		'clear' : True,
		'endswith' : True,
		'loadShape' : True,
		'load' : True,
		'loadNeighborhood' : True,
		'getTime' : True,
		'notify' : True,
		'integer' : True,
		'save' : True,
		'getDBName' : True,
		'sub' : True,
		'saveShape' : True,
		'setDBType' : True,
		'setDBName' : True,
		'len' : True,
		'setPort' : True,
		'setHostName' : True,
		'setUser' : True,
		'setPassword' : True,
		'setTheme' : True,
		'setLayer' : True,
		'setWhereClause' : True,
		'clearAttrName' : True,
		'addAttrName' : True,
		'setReference' : True,
		'getLayerName' : True,
		'init' : True
	}

	luafile = os.path.join(os.path.dirname(__file__), 'data', 'CellularSpace1.lua')
	src = open(luafile).read()
	parser = LuaParser()
	parser.parser(src)
	calls = parser.extract_calls()

	for call in calls:
		assert file_calls[call]	

def test_extract_globals():
	file_globals = {
		'CellularSpace_' : True,
		'metaTableCellularSpace_' : True,	
	}

	luafile = os.path.join(os.path.dirname(__file__), 'data', 'CellularSpace1.lua')
	src = open(luafile).read()
	parser = LuaParser()
	parser.parser(src)
	globals = parser.extract_globals()

	for glob in globals:
		assert file_globals[glob]

def test_extract_local_functions():
	file_local_functions = {
		'coordCoupling' : True,
		'createMooreNeighborhood' : True,
		'createVonNeumannNeighborhood' : True,
		'createNeighborhood' : True,
		'createMxNNeighborhood' : True,
		'spatialCoupling' : True	
	}

	luafile = os.path.join(os.path.dirname(__file__), 'data', 'CellularSpace1.lua')
	src = open(luafile).read()
	parser = LuaParser()
	parser.parser(src)
	functions = parser.extract_local_functions()	

	for func in functions:
		assert file_local_functions[func]

def test_extract_table_functions():
	file_table_functions = {
		'add' : True,
		'createNeighborhood' : True,
		'getCell' : True,
		'get' : True,
		'getCells' : True,
		'getCellByID' : True,
		'load' : True,
		'loadShape' : True,
		'loadNeighborhood' : True,
		'notify' : True,
		'sample' : True,
		'save' : True,
		'saveShape' : True,
		'size' : True,
		'split' : True,
		'synchronize' : True,
		'moore' : True,
		'mxn' : True,
		'vonneumann' : True,
		'coord' : True,
		'__len' : True
	}

	luafile = os.path.join(os.path.dirname(__file__), 'data', 'CellularSpace1.lua')
	src = open(luafile).read()
	parser = LuaParser()
	parser.parser(src)
	functions = parser.extract_table_functions()	

	for func in functions:
		assert file_table_functions[func]
