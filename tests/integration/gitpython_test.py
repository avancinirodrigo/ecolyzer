import os
from os import path
import shutil
from ecolyzer.repository import GitPython


def test_clone():
	git = GitPython()
	to_path = 'calibration'
	if path.exists(to_path):
		shutil.rmtree(to_path, ignore_errors=True)

	git.clone('https://github.com/TerraME/calibration.git', to_path)
	assert GitPython.IsGitRepo(to_path)
	shutil.rmtree(to_path)

def test_clone_branch_default_not_master():
	git = GitPython()
	to_path = 'openhtmltopdf'
	if path.exists(to_path):
		shutil.rmtree(to_path, ignore_errors=True)

	git.clone('https://github.com/danfickle/openhtmltopdf', to_path)
	assert GitPython.IsGitRepo(to_path)
	shutil.rmtree(to_path)
