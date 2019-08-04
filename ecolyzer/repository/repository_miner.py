from pydriller import RepositoryMining, GitRepository
from pydriller.domain.commit import ModificationType
from git import Repo
from ecolyzer.system import File, SourceFile, Operation
from ecolyzer.parser import StaticAnalyzer
from .commit import CommitInfo, Commit
from .modification import ModificationInfo, Modification
from .person import Person
from .author import Author

class RepositoryMiner:
	"""RepositoryMiner"""
	def __init__(self, repo, system):
		self.repo = repo
		self.system = system
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
		self.from_commit = None
		self.to_commit = None
		self.from_tag = None
		self.to_tag = None
		self.only_no_merge = True		

	def commit_interval(self, from_commit, to_commit):
		self.from_commit = from_commit
		self.to_commit = to_commit

	def tag_interval(self, from_tag, to_tag): #, limited_by):
		self.from_tag = from_tag
		self.to_tag = to_tag

	def extract(self, session, hash=None):
		for commit_driller in RepositoryMining(self.repo.path,
							only_modifications_with_file_types=self.source_file_extensions,
							single=hash,
							#from_commit=self.from_commit, to_commit=self.to_commit,
							from_tag=self.from_tag, to_tag=self.to_tag,
							#filepath='CellularSpace.lua',
							only_in_branch=['master'],
							only_no_merge=self.only_no_merge).traverse_commits():
			#session = db.create_session()
			commit_info = self._get_commit_info(commit_driller)
			author = self._check_author(commit_info.author_name, commit_info.author_email)
			commit = Commit(commit_info, author, self.repo)
			session.add(commit)
			for mod_info in commit_info.modifications:
				filepath = self._check_filepath(mod_info)
				if self._is_source_file_ext(File.Extension(filepath)):											
					file = self._check_file(mod_info)
					mod = Modification(mod_info, file, commit)
					if mod.status != 'DELETE':
						srcfile = self._check_source_file(file)
						code_elements = self._extract_code_elements(srcfile, mod.source_code)
						for element in code_elements:
							element.modification = mod
							session.add(element)
					session.add(mod)
			session.commit()

	def _check_source_file(self, file):
		if self.system.source_file_exists(file.fullpath):
			return self.system.get_source_file(file.fullpath)
		else:
			srcfile = SourceFile(file)
			self.system.add_source_file(srcfile)		
			return srcfile

	def _check_filepath(self, mod_info):
		fullpath = mod_info.new_path
		if fullpath == None:
			fullpath = mod_info.old_path
		return fullpath		

	def _check_file(self, mod_info): #TODO: running reverse seems not work
		if self.system.file_exists(mod_info.new_path):
			return self.system.get_file(mod_info.new_path)
		elif mod_info.status == 'DELETE':
			if self.system.file_exists(mod_info.old_path):
				return self.system.get_file(mod_info.old_path)
		else:		
			return self._add_file(mod_info.new_path)

	def _add_file(self, fullpath):
		file = File(fullpath)					
		self.system.add_file(file)
		return file			

	def _update_file(self, old_path, new_file):
		self.system.remove_file(old_path)
		self.system.add_file(new_file)

	def _check_author(self, name, email):
		if self.repo.author_exists(email):
			author = self.repo.get_author(email)
			if name != author.name:
				author.name = name 
			return author
		else:
			person = Person(name, email)
			author = Author(person)					
			self.repo.add_author(author)
			return author

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
			file_mod.status = mod.change_type.name
			file_mod.source_code = mod.source_code
			files_modification.append(file_mod)
		return files_modification

	def _extract_code_elements(self, source_file, source_code):		
		if source_file.ext() == 'lua':
			analyzer = StaticAnalyzer()
			return analyzer.lua_reverse_engineering(source_file, source_code)
		return []

	def is_source_file(self, file):
		return self._is_source_file_ext(file.ext)

	def extract_code_elements(self, source_file, modification):
		return self._extract_code_elements(source_file, modification.source_code)
	
	@staticmethod			
	def IsGitRepo(path):
		try:
			Repo(path).git_dir
		except:
			return False
		return True
