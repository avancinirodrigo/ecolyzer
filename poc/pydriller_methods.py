import os
from pydriller import RepositoryMining

def show_modification(repo_path):
	for commit in RepositoryMining(repo_path, only_in_branches=['master'],
									only_no_merge=True).traverse_commits():
		for mod in commit.modifications:
			if mod.change_type != None:
				if ((mod.change_type.name == "ADD") and (mod.added > 0)):
					path, ext = os.path.splitext(mod.new_path)
					# print(ext)
					# print(mod.new_path)
					if ((ext == ".lua") and (len(mod.methods) > 0)):
						print(mod.new_path)
						print(mod.added)
						print(path)
						#print(mod.source_code)
						for method in mod.methods:
							print('\nmethod:')
							print(method.name)
							print(method.long_name)
							print(method.parameters)
							#print(method.filename)
						#print(mod.source_code)
						return
						
repo_path = 'repo/terrame'
show_modification(repo_path)
