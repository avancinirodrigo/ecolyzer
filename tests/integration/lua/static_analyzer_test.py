import os
from ecolyzer.repository import Repository #TODO: why?
from ecolyzer.system import File, SourceFile
from ecolyzer.parser import StaticAnalyzer

def test_lua_reverse_engineering():
	operations = {
		'CellularSpace' : True,
		'createNeighborhood' : True,
		'add' : True,
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

	calls = {
		'addNeighborhood' : True,
		'addCell' : True,
		'getNeighborhood' : True,
		'caseof' : True,
		'clear' : True,
		'endswith' : True,
		'getTime' : True,
		'integer' : True,
		'getDBName' : True,
		'sub' : True,
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
		'init' : True,
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
		'incompatibleValuesErrorMsg' : True,
		'switch' : True,
		'deprecatedFunctionWarningMsg' : True,
		'Coord' : True,
		'readCSV' : True,
		'tostring' : True,
		'Cell' : True,
		'customErrorMsg' : True,
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

	luafile = os.path.join(os.path.dirname(__file__), '../data', 'CellularSpace1.lua')
	file = File(luafile)
	src_file = SourceFile(file)
	src = open(luafile).read()
	analyzer = StaticAnalyzer()
	code_elements = analyzer.reverse_engineering(src_file, src)

	code_elements_dict = {}
	for element in code_elements:
		code_elements_dict[element.name] = True

	for k in operations.keys():
		assert code_elements_dict[k]

	for k in calls.keys():
		assert code_elements_dict[k]		 

	assert len(code_elements) == len(operations) + len(calls)
	
	for element in code_elements:
		if element.type == 'call':
			assert calls[element.name]
			assert element.name not in operations
		else:
			assert operations[element.name]
			assert element.name not in calls
			
def test_number_of_calls():
	luafile = os.path.join(os.path.dirname(__file__), '../data', 'CellularSpace1.lua')		
	file = File(luafile)
	src_file = SourceFile(file)
	src = open(luafile).read()
	analyzer = StaticAnalyzer()
	assert analyzer.number_of_calls(src_file, src, 'forEachCell') == 16
	assert analyzer.number_of_calls(src_file, src, 'addNeighborhood') == 8
	assert analyzer.number_of_calls(src_file, src, 'Cell') == 2