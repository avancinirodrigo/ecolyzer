from ecolyzer.repository import File

def test_fullpath():
	filepath1 = 'some/path/file1.exa'
	filepath2 = 'file2.exb'
	filepath3 = 'file3'

	file1 = File(filepath1)
	assert file1.name == 'file1'
	assert file1.path == 'some/path'
	assert file1.ext == 'exa'
	assert file1.fullpath() == filepath1

	file2 = File(filepath2)
	assert file2.name == 'file2'
	assert file2.path == ''
	assert file2.ext == 'exb'
	assert file2.fullpath() == filepath2

	file3 = File(filepath3)
	assert file3.name == 'file3'
	assert file3.path == ''
	assert file3.ext == ''
	assert file3.fullpath() == filepath3
