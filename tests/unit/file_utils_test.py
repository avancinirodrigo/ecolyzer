from ecolyzer.utils import FileUtils


def test_split():
	path, name, ext = FileUtils.split('some/path/file.ext')
	assert path == 'some/path'
	assert name == 'file'
	assert ext == 'ext'


def test_extension():
	assert FileUtils.extension('some/path/file.ext') == 'ext'
	assert FileUtils.extension('file') == ''	