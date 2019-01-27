import pytest

from ecolyzer.system import SourceFile

def test_constructor():
	fullpath = 'some/path/file.ext'
	src = SourceFile(fullpath)
	assert src.fullpath == fullpath
	assert src.ext == 'ext'
	assert src.path == 'some/path'
	assert src.name == 'file'