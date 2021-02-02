from ecolyzer.repository import Repository  # TODO: why import module?
from ecolyzer.system import File


def test_fullpath():
	filepath1 = 'some/path/file1.exa'
	filepath2 = 'file2.exb'
	filepath3 = 'file3'
	filepath4 = 'file4.ext'

	file1 = File(filepath1)
	assert file1.name == 'file1'
	assert file1.path == 'some/path'
	assert file1.ext == 'exa'
	assert file1.fullpath == filepath1

	file2 = File(filepath2)
	assert file2.name == 'file2'
	assert file2.path == ''
	assert file2.ext == 'exb'
	assert file2.fullpath == filepath2

	file3 = File(filepath3)
	assert file3.name == 'file3'
	assert file3.path == ''
	assert file3.ext == ''
	assert file3.fullpath == filepath3

	file4 = File(filepath4)
	assert file4.name == 'file4'
	assert file4.path == ''
	assert file4.ext == 'ext'
	assert file4.fullpath == filepath4	


def test_more_than_one_dot():
	file_2dots = File('file.ex.t')
	assert file_2dots.name == 'file.ex'
	assert file_2dots.ext == 't'

	file_3dots = File('path/file.e.x.t')
	assert file_3dots.name == 'file.e.x'
	assert file_3dots.ext == 't'


def test_dot_at_begin():
	file1 = File('.file')
	assert file1.name == '.file'
	assert file1.ext == ''
	assert file1.fullpath == '.file'

	file2 = File('path/.file.ext')
	assert file2.name == '.file'
	assert file2.ext == 'ext' 
	assert file2.path == 'path'
	assert file2.fullpath == 'path/.file.ext' 

	file3 = File('some/path/.file.e.x.t')
	assert file3.name == '.file.e.x'
	assert file3.ext == 't' 
	assert file3.path == 'some/path'
	assert file3.fullpath == 'some/path/.file.e.x.t' 


def test_without_ext():
	file1 = File('some/path/noextfile')
	assert file1.fullpath == 'some/path/noextfile'

	file2 = File('noextfile')
	assert file2.fullpath == 'noextfile'
