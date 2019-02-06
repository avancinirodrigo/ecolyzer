from pydriller import RepositoryMining, GitRepository
from ecolyzer.repository.commit import CommitInfo

class RepositoryMiner:
	"""RepositoryMiner"""
	def __init__(self, repo_path):
		self.repo_path = repo_path
		self.source_file_extensions = [
			#'c', 'cc', 'cpp', 'h', 'hpp', 'hxx',
			#'ui', 'qrc',
			'lua',
			#'cmake', 'in',
			#'photo',
			#'sh',
			#'bat',
			#'rc',
			# 'log', # verificar
			#'lp', 'css',
		]		

	def extract(self):
		for commit in RepositoryMining(repo_path, only_in_branches=['master'],
									only_no_merge=True).traverse_commits():

			for mod in commit.modifications:
				if mod.change_type != None:
					if ((mod.change_type.name == "ADD") and (mod.added > 0)):
						git_file = GitFile(mod.new_path)
						git_file.added = mod.added
						git_files.append(git_file)

		return git_files
		
	def get_commit_info(self, hash):
		repo_driller = GitRepository(self.repo_path)
		commit_driller = repo_driller.get_commit(hash)
		commit_info = CommitInfo(hash)
		commit_info.date = commit_driller.author_date
		commit_info.msg = commit_driller.msg
		author_driller = commit_driller.author
		commit_info.author = author_driller.name
		commit_info.author_email = author_driller.email
		return commit_info





