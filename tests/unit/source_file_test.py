import pytest	
from ecolyzer.repository import Repository
from ecolyzer.system import File, SourceFile, Function

def test_add_function_same_name():
	filepath = 'some/path/file.src'
	file = File(filepath)
	src_file = SourceFile(file)

	f1 = Function('get')
	src_file.add_function(f1)	

	with pytest.raises(Exception) as e:
		src_file.add_function(f1)
	assert (('Function \'get\' is already present')
			in str(e.value))		

def test_function_exists():
	filepath = 'some/path/file.src'
	file = File(filepath)
	src_file = SourceFile(file)

	f1 = Function('get')
	src_file.add_function(f1)	

	assert src_file.function_exists(f1)
	