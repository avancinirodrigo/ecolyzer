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

# def test_clone_tag(): #TODO
# 	git = GitPython()
# 	to_path = 'scribejava'
# 	if path.exists(to_path):
# 		shutil.rmtree(to_path, ignore_errors=True)

# 	git.clone('https://github.com/scribejava/scribejava', to_path, branch='scribejava-8.0.0')
# 	repo = Repository(to_path)
# 	assert repo.branch == ''
# 	shutil.rmtree(to_path)	
