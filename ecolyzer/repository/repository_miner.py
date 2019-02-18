from enum import Enum
from pydriller import RepositoryMining, GitRepository
from pydriller.domain.commit import ModificationType
from ecolyzer.system import SourceFile, Function
from ecolyzer.parser import LuaParser
from .commit import CommitInfo, Commit
from .modification import ModificationInfo, Modification
from .author import Author
from .file import File

class RepositoryMiner:
	"""RepositoryMiner"""
	def __init__(self, repo):
		self.repo = repo
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

	def extract(self, session, hash):
		for commit_driller in RepositoryMining(self.repo.path,
							only_modifications_with_file_types=self.source_file_extensions,
							single=hash,
							only_in_branch=['master']).traverse_commits():
			#session = db.create_session()
			commit_info = self._get_commit_info(commit_driller)
			author = Author(commit_info.author_name, commit_info.author_email)
			commit = Commit(commit_info, author, self.repo)
			session.add(commit)
			for mod_info in commit_info.modifications:
				file = File(mod_info.new_path)
				mod = Modification(mod_info, file, commit)
				if self._is_source_file_ext(file.ext):
					srcfile = SourceFile(file)
					session.add(srcfile)
					functions = self._extract_functions(srcfile, mod.source_code)
					for func in functions:
						function = Function(func, srcfile)
						session.add(function)
				session.add(mod)
			session.commit()

	def _is_source_file_ext(self, ext):
		return ext in self.source_file_extensions

	def get_commit_info(self, hash):
		repo_driller = GitRepository(self.repo.path)
		commit_driller = repo_driller.get_commit(hash)
		return self._get_commit_info(commit_driller)

	def _get_commit_info(self, commit_driller):
		commit_info = CommitInfo(commit_driller.hash)
		commit_info.date = commit_driller.author_date
		commit_info.msg = commit_driller.msg
		author_driller = commit_driller.author
		commit_info.author_name = author_driller.name
		commit_info.author_email = author_driller.email
		commit_info.modifications = self._get_modifications_info(commit_driller.modifications)
		#commit_info.project_name = commit_driller.project_name
		#commit_info.project_path = commit_driller.project_path
		#commit_info.merge = commit_driller.merge
		#commit_info.in_main_branch = commit_driller.in_main_branch
		return commit_info

	def _get_modifications_info(self, modifications):
		files_modification = []
		for mod in modifications:
			file_mod = ModificationInfo(mod.filename)
			file_mod.old_path = mod.old_path
			file_mod.new_path = mod.new_path
			file_mod.added = mod.added
			file_mod.removed = mod.removed
			file_mod.type = mod.change_type.name
			file_mod.source_code = mod.source_code
			files_modification.append(file_mod)
		return files_modification

	def _extract_functions(self, source_file, source_code):
		if source_file.ext == 'lua':
			parser = LuaParser()
			parser.parser(source_code)
			return parser.extract_functions()
		return []