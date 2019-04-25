import pytest	
from ecolyzer.repository import Repository
from ecolyzer.system import File, SourceFile, Operation

def test_add_operation_same_name():
	filepath = 'some/path/file.src'
	file = File(filepath)
	src_file = SourceFile(file)

	f1 = Operation('get')
	src_file.add_operation(f1)

	with pytest.raises(Exception) as e:
		src_file.add_operation(f1)
	assert (('Operation \'get\' is already present')
			in str(e.value))		

def test_operation_exists():
	filepath = 'some/path/file.src'
	file = File(filepath)
	src_file = SourceFile(file)

	f1 = Operation('get')
	src_file.add_operation(f1)	

	assert src_file.operation_exists(f1.name)
	