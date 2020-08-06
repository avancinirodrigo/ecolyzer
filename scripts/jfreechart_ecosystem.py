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

print('Extracting ' + sys1.name)
miner = RepositoryMiner(repo1, sys1)
miner.add_ignore_dir_with('test')	
miner.extract_last_commits(session)

repo2 = Repository('repo/projectforge')
sys2 = System('ProjectForge', repo2)
print('Extracting ' + sys2.name)
miner = RepositoryMiner(repo2, sys2)		
miner.extract_last_commits(session)

repo3 = Repository('repo/metasfresh')
sys3 = System('metasfresh', repo3)
print('Extracting ' + sys3.name)
miner = RepositoryMiner(repo3, sys3)	
miner.extract_last_commits(session)

repo4 = Repository('repo/ta4j')
sys4 = System('Ta4j ', repo4)
print('Extracting ' + sys4.name)
miner = RepositoryMiner(repo4, sys4)	
miner.extract_last_commits(session)

repo5 = Repository('repo/oshi')
sys5 = System('OSHI', repo5)
print('Extracting ' + sys5.name)
miner = RepositoryMiner(repo5, sys5)	
miner.extract_last_commits(session)

repo6 = Repository('repo/trick')
sys6 = System('Trick', repo6)
print('Extracting ' + sys6.name)
miner = RepositoryMiner(repo6, sys6)	
miner.extract_last_commits(session)

repo7 = Repository('repo/moeaframework')
sys7 = System('MOEAFramework', repo7)
print('Extracting ' + sys7.name)
miner = RepositoryMiner(repo7, sys7)	
miner.extract_last_commits(session)

ecosystem = Ecosystem()

ecolyzer = EcosystemAnalyzer(ecosystem)
ecolyzer.make_relations(sys2, sys1, session)
ecolyzer.make_relations(sys3, sys1, session)
ecolyzer.make_relations(sys4, sys1, session)
ecolyzer.make_relations(sys5, sys1, session)
ecolyzer.make_relations(sys6, sys1, session)
ecolyzer.make_relations(sys7, sys1, session)

session.close()