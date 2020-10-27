from ecolyzer.repository import GitPython, GitHub, Repository,\
								RepositoryMiner
from ecolyzer.system import System
from ecolyzer.utils import FileUtils
from ecolyzer.ecosystem import Ecosystem, EcosystemAnalyzer


class MappingEcosystemDependents:
	"""MappingEcosystemDependents"""
	def __init__(self, repo_url: str, **kwargs):
		self._repo_url = repo_url
		self._branch = kwargs.get('branch', 'master')
		self._stars = kwargs.get('stars', 0)
		self._ignore_dirs_with = kwargs.get('ignore_dirs_with', [])
		self._system_name = kwargs.get('system_name')
		self._ecosystem_name = kwargs.get('ecosystem_name')

	def execute(self, dataaccess):
		gh = GitHub(self._repo_url)
		dependents = gh.dependents(self._stars)
		git = GitPython()
		git.clone(self._repo_url, branch=self._branch)

		central_repo = Repository(git.path)

		if not self._system_name:
			self._system_name = central_repo.name

		central_system = System(self._system_name, central_repo)
		dataaccess.add(central_system)

		miner = RepositoryMiner(central_repo, central_system)
		self._ignore_dirs(miner)
		miner.extract_last_commits(dataaccess)		
		FileUtils.rmdir(git.path)

		if not self._ecosystem_name:
			self._ecosystem_name = central_repo.name

		ecosystem = Ecosystem(self._ecosystem_name)
		dataaccess.add(ecosystem)
		ecolyzer = EcosystemAnalyzer(ecosystem)
		for dep in dependents:
			gp = GitPython()
			gp.clone(dep.url, dep.repo)
			repo = Repository(gp.path)
			sys = System(repo.name, repo)
			miner = RepositoryMiner(repo, sys)
			miner.extract_last_commits(dataaccess)	
			FileUtils.rmdir(gp.path)
			ecolyzer.make_relations(sys, central_system, dataaccess)

	def _get_dependents(self):
		gh = GitHub()
		return gh.dependents(self.repo_url, self.stars)		

	def _ignore_dirs(self, miner):
		for dir in self._ignore_dirs_with:
			miner.add_ignore_dir_with(dir)
