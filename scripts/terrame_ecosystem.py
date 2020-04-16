import os
from ecolyzer.ecosystem import EcosystemAnalyzer
from ecolyzer.system import System
from ecolyzer.repository import Repository, Person, Author, RepositoryMiner, GitPython
from ecolyzer.dataaccess import SQLAlchemyORM
from ecolyzer.ecosystem import Ecosystem

db_url = os.environ.get('DATABASE_URL') or \
	'postgresql://postgres:postgres@localhost:5432/terrame_ecosystem'
db = SQLAlchemyORM(db_url)
db.create_all(True)
session = db.create_session()

repo1 = Repository('repo/terrame')
sys1 = System('TerraME', repo1)

session.add(repo1)
session.add(sys1)

miner = RepositoryMiner(repo1, sys1)
miner.add_ignore_dir_with('test')
miner.add_ignore_dir_with('example')	
miner.add_ignore_dir_with('data')	
miner.add_ignore_dir_with('images')	
miner.add_ignore_dir_with('zerobrane')	
miner.extract_last_commits(session, '2.0-RC-8')

repo2 = Repository('repo/ca')
sys2 = System('ca', repo2)
miner = RepositoryMiner(repo2, sys2)	
miner.extract_last_commits(session)

repo3 = Repository('repo/calibration')
sys3 = System('calibration', repo3)
miner = RepositoryMiner(repo3, sys3)	
miner.extract_last_commits(session)

repo4 = Repository('repo/logo')
sys4 = System('logo', repo4)
miner = RepositoryMiner(repo4, sys4)	
miner.extract_last_commits(session)

repo5 = Repository('repo/rstats')
sys5 = System('rstats', repo5)
miner = RepositoryMiner(repo5, sys5)	
miner.extract_last_commits(session)

repo6 = Repository('repo/gpm')
sys6 = System('gpm', repo6)
miner = RepositoryMiner(repo6, sys6)	
miner.extract_last_commits(session)

repo7 = Repository('repo/publish')
sys7 = System('publish', repo7)
miner = RepositoryMiner(repo7, sys7)	
miner.extract_last_commits(session)

repo8 = Repository('repo/sci')
sys8 = System('sci', repo8)
miner = RepositoryMiner(repo8, sys8)	
miner.extract_last_commits(session)

repo9 = Repository('repo/urban')
sys9 = System('urban', repo9)
miner = RepositoryMiner(repo9, sys9)	
miner.extract_last_commits(session)

repo10 = Repository('repo/ford')
sys10 = System('ford', repo10)
miner = RepositoryMiner(repo10, sys10)	
miner.extract_last_commits(session)

repo11 = Repository('repo/sysdyn')
sys11 = System('sysdyn', repo11)
miner = RepositoryMiner(repo11, sys11)	
miner.extract_last_commits(session)

repo12 = Repository('repo/luccme')
sys12 = System('luccme', repo12)
miner = RepositoryMiner(repo12, sys12)	
miner.extract_last_commits(session)

repo13 = Repository('repo/inpeem')
sys13 = System('impeem', repo13)
miner = RepositoryMiner(repo13, sys13)	
miner.extract_last_commits(session)

ecosystem = Ecosystem()

ecolyzer = EcosystemAnalyzer(ecosystem)
ecolyzer.make_relations(sys2, sys1, session)
ecolyzer.make_relations(sys3, sys1, session)
ecolyzer.make_relations(sys4, sys1, session)
ecolyzer.make_relations(sys5, sys1, session)
ecolyzer.make_relations(sys6, sys1, session)
ecolyzer.make_relations(sys7, sys1, session)
ecolyzer.make_relations(sys8, sys1, session)
ecolyzer.make_relations(sys9, sys1, session)
ecolyzer.make_relations(sys10, sys1, session)
ecolyzer.make_relations(sys11, sys1, session)
ecolyzer.make_relations(sys12, sys1, session)
ecolyzer.make_relations(sys13, sys1, session)

session.close()