from pydriller import RepositoryMining
from gitdriller.git_file import GitFile

class PyDriller(object):
	def __new__(cls, *args, **kwargs):
		if not hasattr(cls, '_instance'):
			cls._instance = super(PyDriller, cls).__new__(cls, *args, **kwargs)
		return cls._instance
		
	def get_added_files_between_tags(self, repo_path, from_tag, to_tag):
		git_files = []
		for commit in RepositoryMining(repo_path, only_in_branches=['master'], 
									only_no_merge=True, from_tag=from_tag, 
									to_tag=to_tag).traverse_commits():
			for m in commit.modifications:
				if m.change_type != None:
					git_file = GitFile(m.filename)
					if ((m.change_type.name == "ADD") and (m.added > 0)):	
						git_file.added = m.added
						git_files.append(git_file)												
		
		return git_files
		
