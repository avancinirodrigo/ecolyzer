import pytest
from ecolyzer.system import System, File
from ecolyzer.repository import Repository, GitPython


def test_add_file_same_fullpath(mocker):
	mocker.patch.object(GitPython, 'IsGitRepo', return_value=True)
	mocker.patch.object(GitPython, 'CurrentBranch', return_value='master')
	repo = Repository('repo/terrame')
	sys = System('terrame', repo)

	file1 = File('path/file.ext')
	file2 = File('path/file.ext')
	sys.add_file(file1)

	with pytest.raises(Exception) as e:
		sys.add_file(file2)
	assert (('File \'path/file.ext\' is already present')
			in str(e.value))		


def test_file_exists(mocker):
	mocker.patch.object(GitPython, 'IsGitRepo', return_value=True)
	mocker.patch.object(GitPython, 'CurrentBranch', return_value='master')
	repo = Repository('repo/terrame')
	sys = System('terrame', repo)

	file = File('path/file.ext')
	sys.add_file(file)	

	assert sys.file_exists(file.fullpath)
