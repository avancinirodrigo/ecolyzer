from git import Repo

class GitPython:
	"""GitPython"""
	def __init__(self, path):
		self.repo = Repo(path)
		self.git_dir = self.repo.git_dir

	def commit_hashs(self, max_count=None, branch='master'):
		commits = list(self.repo.iter_commits(branch, max_count=max_count))
		return (commit.hexsha for commit in commits)

	def commit_hashs_reverse(self, max_count=None, branch='master'):
		commits = list(self.repo.iter_commits(branch, reverse=True))		
		if max_count:
			return (commits[i].hexsha for i in range(max_count))
		else:
			return (commit.hexsha for commit in commits)
		
	@staticmethod
	def IsGitRepo(path):
		try:
			Repo(path).git_dir
		except:
			return False
		return True		
		