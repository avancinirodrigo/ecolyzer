import os
from ecolyzer.system import System
from ecolyzer.repository import Repository, Person, Author, \
							RepositoryMiner, GitPython
from ecolyzer.dataaccess import SQLAlchemyORM
from ecolyzer.ecosystem import Ecosystem, EcosystemAnalyzer
from ecolyzer.repository import GitPython


db_url = 'postgresql://postgres:postgres@localhost:5432/jfreechart_ecosystem_top5'
db = SQLAlchemyORM(db_url)
db.create_all(True)
session = db.create_session()

to_path = 'repo/jfreechart'
git = GitPython()
git.clone('https://github.com/jfree/jfreechart', to_path)
repo1 = Repository(to_path)
sys1 = System('JFreeChart', repo1)

session.add(repo1)
session.add(sys1)

print('Extracting ' + sys1.name)
miner = RepositoryMiner(repo1, sys1)
miner.add_ignore_dir_with('test')	
miner.extract_last_commits(session)

to_path = 'repo/jenkins'
git = GitPython()
git.clone('https://github.com/jenkinsci/jenkins', to_path)
repo2 = Repository(to_path)
sys2 = System('Jenkins', repo2)
print('Extracting ' + sys2.name)
miner = RepositoryMiner(repo2, sys2)		
miner.extract_last_commits(session)

to_path = 'repo/geoserver'
git = GitPython()
git.clone('https://github.com/geoserver/geoserver', to_path)
repo3 = Repository(to_path)
sys3 = System('GeoServer', repo3)
print('Extracting ' + sys3.name)
miner = RepositoryMiner(repo3, sys3)	
miner.extract_last_commits(session)

to_path = 'repo/gephi'
git = GitPython()
git.clone('https://github.com/gephi/gephi', to_path)
repo4 = Repository(to_path)
sys4 = System('Gephi', repo4)
print('Extracting ' + sys4.name)
miner = RepositoryMiner(repo4, sys4)	
miner.extract_last_commits(session)

to_path = 'repo/Movie_Recommend'
git = GitPython()
git.clone('https://github.com/LuckyZXL2016/Movie_Recommend', to_path)
repo5 = Repository(to_path)
sys5 = System('Movie_Recommend', repo5)
print('Extracting ' + sys5.name)
miner = RepositoryMiner(repo5, sys5)	
miner.extract_last_commits(session)

to_path = 'repo/struts'
git = GitPython()
git.clone('https://github.com/apache/struts', to_path)
repo6 = Repository(to_path)
sys6 = System('Struts', repo6)
print('Extracting ' + sys6.name)
miner = RepositoryMiner(repo6, sys6)	
miner.extract_last_commits(session)

ecosystem = Ecosystem()

ecolyzer = EcosystemAnalyzer(ecosystem)
print('Relationships', sys1.name, sys2.name)
ecolyzer.make_relations(sys2, sys1, session)
print('Relationships', sys1.name, sys3.name)
ecolyzer.make_relations(sys3, sys1, session)
print('Relationships', sys1.name, sys4.name)
ecolyzer.make_relations(sys4, sys1, session)
print('Relationships', sys1.name, sys5.name)
ecolyzer.make_relations(sys5, sys1, session)
print('Relationships', sys1.name, sys6.name)
ecolyzer.make_relations(sys6, sys1, session)

session.close()
