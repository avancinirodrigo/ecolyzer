import pytest
from ecolyzer.repository import Repository


def test_invalid_repo_path():
	with pytest.raises(Exception) as e:
		Repository('invalid/repo')
	assert (('Invalid repository path \'invalid/repo\'')
			in str(e.value))	
