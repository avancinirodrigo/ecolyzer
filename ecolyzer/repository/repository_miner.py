import sys
from sqlalchemy.orm.exc import NoResultFound
from pydriller import RepositoryMining, GitRepository
from pydriller.domain.commit import ModificationType
from git import Repo
from ecolyzer.system import File, SourceFile, Operation
from ecolyzer.parser import StaticAnalyzer
from ecolyzer.dataaccess import NullSession
from .commit import CommitInfo, Commit
from .modification import ModificationInfo, Modification
from .person import Person
from .author import Author

class RepositoryMiner:
	"""RepositoryMiner"""
	def __init__(self, repo, system):
		self.repo = repo
		self.system = system
		self.source_file_extensions = {}
		self.source_file_extensions['lua'] = 'lua'
		self.ignore_dir_with = {}
		self.from_commit = None
		self.to_commit = None
		self.from_tag = None
		self.to_tag = None
		self.only_no_merge = True		

	def commit_interval(self, from_commit, to_commit):
		self.from_commit = from_commit
		self.to_commit = to_commit

	def tag_interval(self, from_tag, to_tag):
		self.from_tag = from_tag
		self.to_tag = to_tag

	def extract(self, session, hash=None, max_count=sys.maxsize):
		count = 0
		for commit_driller in RepositoryMining(path_to_repo=[self.repo.path],
							only_modifications_with_file_types=self.source_file_extensions,
							single=hash,
							#from_commit=self.from_commit, to_commit=self.to_commit,
							from_tag=self.from_tag, to_tag=self.to_tag,
							#filepath='CellularSpace.lua',
							only_in_branch=['master'],
							only_no_merge=self.only_no_merge).traverse_commits():
			self._extract_from_driller(commit_driller, session)
			count += 1
			if count == max_count:
				session.commit()
				return	
			session.commit()

	def _extract_from_driller(self, commit_driller, session):
		commit_info = self._get_commit_info(commit_driller)
		author = self._check_author(session, commit_info.author_name, commit_info.author_email)
		commit = Commit(commit_info, author, self.repo)
		for mod_info in commit_info.modifications:
			filepath = self._check_filepath(mod_info)
			if self._is_valid_source(filepath):											
				file = self._check_file(mod_info)
				mod = Modification(mod_info, file, commit)
				if mod.status != 'DELETE':
					srcfile = self._check_source_file(file)
					code_elements = self._extract_code_elements(srcfile, mod.source_code)
					for element in code_elements:
						code_element = self._check_code_element(session, srcfile, element, mod)
				session.add(mod)

	def extract_last_commits(self, session=NullSession(), rev=None):
		repo = Repo(self.repo.path)
		blobs = self._repo_file_blobs(repo)
		for blob in blobs:
			commit = self._last_commit_from_path(blob.path, repo, rev)	
			commit_info = self._get_commit_info_from_gitpython(commit)
			author = self._check_author(session, commit_info.author_name, commit_info.author_email)
			commit = self._check_commit(commit_info, author)
			mod_info = self._get_modification_from_gitpython(blob)
			file = self._check_file(mod_info)
			mod = Modification(mod_info, file, commit)
			srcfile = self._check_source_file(file)
			code_elements = self._extract_code_elements(srcfile, mod.source_code)
			for element in code_elements:
				code_element = self._check_code_element(session, srcfile, element, mod)
			session.add(mod)
		session.commit()

	def _get_commit_info_from_gitpython(self, commit):
		commit_info = CommitInfo(commit.hexsha)
		commit_info.date = commit.authored_datetime
		commit_info.msg = commit.message
		committer = commit.committer
		commit_info.author_name = committer.name
		commit_info.author_email = committer.email
		return commit_info

	def _get_modification_from_gitpython(self, blob):
		file_mod = ModificationInfo(blob.path)
		#file_mod.old_path = mod.old_path
		file_mod.new_path = blob.path
		#file_mod.status = mod.change_type.name 
		source_code = self._get_blob_source_code(blob)
		file_mod.source_code = source_code
		file_mod.added = self._count_lines_of_code(blob.path, source_code)
		file_mod.removed = 0
		file_mod.nloc = file_mod.added
		return file_mod

	def _count_lines_of_code(self, filepath, source_code):
		analyzer = StaticAnalyzer()
		metrics = analyzer.lua_metrics(filepath, source_code)
		return metrics.nloc()

	def _last_commit_from_path(self, fullpath, repo, rev):
		return list(repo.iter_commits(rev=rev, paths=fullpath, max_count=1))[0]

	def extract_current_files(self, session=NullSession()):
		repo = Repo(self.repo.path)
		tree = repo.tree()
		blobs = self._repo_file_blobs(repo)
		self._extract_current_files(blobs, session)

	def _repo_file_blobs(self, repo):
		tree = repo.tree()
		blobs = []
		for dir in tree.trees:
			self._navigate_dirs(dir.trees, blobs)
			self._get_file_blobs(dir, blobs)
		return blobs

	def _navigate_dirs(self, trees, blobs):
		if len(trees) > 0:
			for dir in trees:
				self._navigate_dirs(dir.trees, blobs)
				self._get_file_blobs(dir, blobs)

	def _get_file_blobs(self, dir, blobs):
		for blob in dir.blobs:
			if self._is_valid_source(blob.path):		
				blobs.append(blob)

	def _valid_dir(self, dirpath):
		for dir in self.ignore_dir_with:
			if dir in dirpath:
				return False
		return True

	def add_ignore_dir_with(self, dir):
		self.ignore_dir_with[dir] = dir

	def _is_valid_source(self, filepath):
		path, filename, ext = File.Split(filepath)
		return (self._valid_ext(ext) 
					and self._valid_dir(path))		

	def _extract_current_files(self, blobs, session):
		for blob in blobs:
			if self._is_valid_source(blob.path):
				file = self._add_file(blob.path)
				srcfile = self._check_source_file(file)
				srccode = self._get_blob_source_code(blob)
				code_elements = self._extract_code_elements(srcfile, srccode)
				for element in code_elements:
					code_element = self._check_code_element(session, srcfile, element)
				session.add(srcfile)
		session.commit()

	def _get_blob_source_code(self, blob):
		data = blob.data_stream.read()
		return data.decode('utf-8', errors='ignore') #TODO: handle instead ignore

	def _create_modification(self, source_file, source_code): #TODO: use in extract_current_files		
		mod = ModificationInfo(mod.filename)
		mod.new_path = source_file.fullpath()
		mod.source_code = source_code
					
	def _check_code_element(self, session, source_file, element, modification=None):
		if not source_file.code_element_exists(element):
			source_file.add_code_element(element)
			element.modification = modification
		else:
			session.expunge(element)
		return source_file.code_element_by_key(element.key)	

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

	def _check_author(self, session, name, email):
		if self.repo.author_exists(email):
			author = self.repo.get_author(email)
			if name != author.name:
				author.name = name 
			return author
		else:
			author = None
			try:
				author = session.query(Author).\
							filter(Person.id == Author.person_id).\
							filter(Person.email == email).one()
			except NoResultFound:
				pass
			if author:
				return author
			else:
				person = Person(name, email)
				author = Author(person)					
				self.repo.add_author(author)
				return author

	def _check_commit(self, commit_info, author):
		if not self.repo.commit_exists(commit_info.hash):
			commit = Commit(commit_info, author, self.repo)
			self.repo.add_commit(commit)
		return self.repo.get_commit(commit_info.hash)	

	def _valid_ext(self, ext):
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
		if source_file.ext == 'lua':
			analyzer = StaticAnalyzer()
			return analyzer.lua_reverse_engineering(source_file, source_code)
		return []

	def is_source_file(self, file):
		return self._valid_ext(file.ext)

	def extract_code_elements(self, source_file, modification):
		return self._extract_code_elements(source_file, modification.source_code)

	@staticmethod
	def HashHeadCommit(path):
		return Repo(path).head.commit.hexsha	