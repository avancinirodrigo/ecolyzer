import os
from os import path
import shutil
from ecolyzer.repository import GitPython


def test_clone():
	git = GitPython()
	to_path = 'repo/calibration'
	if path.exists(to_path):
		shutil.rmtree(to_path, ignore_errors=True)

	git.clone('https://github.com/TerraME/calibration.git', to_path)
	assert GitPython.IsGitRepo(to_path)
	shutil.rmtree(to_path)


