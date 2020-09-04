from urllib.parse import urlparse
from git import Repo
from ecolyzer.utils import FileUtils


class GitPython:
	"""GitPython"""
	def __init__(self, path=None):
		if path:
			self.repo = Repo(path)
			self._is_git_repo(self.repo)

	def _is_git_repo(self, repo):
		self.repo.git_dir

	def commit_hashs(self, max_count=None, branch='master'):
		commits = list(self.repo.iter_commits(branch, max_count=max_count))
		return (commit.hexsha for commit in commits)

	def commit_hashs_reverse(self, max_count=None, branch='master'):
		commits = list(self.repo.iter_commits(branch, reverse=True))		
		if max_count:
			return list(commits[i].hexsha for i in range(max_count))
		else:
			return list(commit.hexsha for commit in commits)

	def clone(self, url: str, to_path: str=None, branch='master'):
		if not to_path:
			path = urlparse(url).path
			to_path = FileUtils.last_dir(path)
		self.path = to_path
		try:
			self.repo = Repo.clone_from(url, self.path, branch=branch)
		except Exception as e:
			if 'already exists' in str(e):
				FileUtils.rmdir(self.path)
				self.repo = Repo.clone_from(url, self.path, branch=branch)
			else:
				raise e
		
	@staticmethod
	def IsGitRepo(path):
		try:
			Repo(path).git_dir 
		except:
			return False
		return True		
		