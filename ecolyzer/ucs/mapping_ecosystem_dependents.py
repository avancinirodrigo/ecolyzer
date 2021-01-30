from ecolyzer.repository import GitPython, GitHub, Repository,\
								RepositoryMiner
from ecolyzer.system import System
from ecolyzer.utils import FileUtils
from ecolyzer.ecosystem import Ecosystem, EcosystemAnalyzer


class MappingEcosystemDependents:
	"""MappingEcosystemDependents"""
	def __init__(self, repo_url: str, **kwargs):
		self._repo_url = repo_url
		self._branch = kwargs.get('branch', None)
		self._stars = kwargs.get('stars', 0)
		self._forks = kwargs.get('forks', 0)
		self._ignore_dirs_with = kwargs.get('ignore_dirs_with', [])
		self._system_name = kwargs.get('system_name')
		self._ecosystem_name = kwargs.get('ecosystem_name')

	def execute(self, dataaccess):
		gh = GitHub(self._repo_url)
		dependents = gh.dependents(self._stars, self._forks)
		git = GitPython()
		central_repo_path = git.url_to_path(self._repo_url)
		existing_repos = self._get_repos(dataaccess)
		central_system = None
		ecosystem = None
		if central_repo_path in existing_repos:
			central_repo = existing_repos[central_repo_path]
			if not self._system_name:
				self._system_name = central_repo.name			
			central_system = dataaccess.query(System).\
						filter_by(name=self._system_name).one()
			ecosystem = dataaccess.query(Ecosystem).\
						filter_by(name=self._ecosystem_name).one()
		else:
			git.clone(self._repo_url, branch=self._branch)  # TODO: check if it exists
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
			dataaccess.commit()
			existing_repos[central_repo.path] = central_repo

		ecolyzer = EcosystemAnalyzer(ecosystem)
		count = 0
		for dep in dependents:
			if dep.repo not in existing_repos:
				gp = GitPython()
				gp.clone(dep.url, dep.repo)
				repo = Repository(gp.path)
				sys = System(repo.name, repo)
				count += 1
				print(count, 'Analysing', sys.name, dep.url)
				miner = RepositoryMiner(repo, sys)
				miner.extract_last_commits(dataaccess)	
				FileUtils.rmdir(gp.path)
				ecolyzer.make_relations(sys, central_system, dataaccess)
				existing_repos[repo.path] = repo

	def _get_dependents(self):
		gh = GitHub()
		return gh.dependents(self.repo_url, self.stars)		

	def _ignore_dirs(self, miner):
		for dir in self._ignore_dirs_with:
			miner.add_ignore_dir_with(dir)

	def _get_repos(self, dataaccess):
		repos = dataaccess.query(Repository).all()
		repos_dict = {}
		for repo in repos:
			repos_dict[repo.path] = repo
		return repos_dict
