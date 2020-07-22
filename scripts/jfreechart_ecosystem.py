import os
from ecolyzer.ecosystem import EcosystemAnalyzer
from ecolyzer.system import System
from ecolyzer.repository import Repository, Person, Author, \
							RepositoryMiner, GitPython
from ecolyzer.dataaccess import SQLAlchemyORM
from ecolyzer.ecosystem import Ecosystem

db_url = 'postgresql://postgres:postgres@localhost:5432/jfreechart_ecosystem'
db = SQLAlchemyORM(db_url)
db.create_all(True)
session = db.create_session()

repo1 = Repository('repo/jfreechart')
sys1 = System('JFreeChart', repo1)

session.add(repo1)
session.add(sys1)

miner = RepositoryMiner(repo1, sys1)
miner.add_ignore_dir_with('test')	
miner.extract_last_commits(session)

repo2 = Repository('repo/projectforge-webapp')
sys2 = System('ProjectForge', repo2)

miner = RepositoryMiner(repo2, sys2)		
miner.extract_last_commits(session)

ecosystem = Ecosystem()

ecolyzer = EcosystemAnalyzer(ecosystem)
ecolyzer.make_relations(sys2, sys1, session)

session.close()