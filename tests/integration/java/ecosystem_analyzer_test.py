from ecolyzer.ecosystem import EcosystemAnalyzer, Relationship
from ecolyzer.system import System
from ecolyzer.repository import Repository, Person, Author, RepositoryMiner, GitPython
from ecolyzer.dataaccess import SQLAlchemyORM
from ecolyzer.ecosystem import Ecosystem


def test_relations_last_commits():
	db_url = 'postgresql://postgres:postgres@localhost:5432/ecolyzer_java_relations_last'
	db = SQLAlchemyORM(db_url)
	db.create_all(True)
	session = db.create_session()

	repo1 = Repository('repo/jfreechart')
	sys1 = System('JFreeChart', repo1)

	session.add(repo1)
	session.add(sys1)

	miner = RepositoryMiner(repo1, sys1)
	miner.add_ignore_dir_with('chart')
	miner.add_ignore_dir_with('test')	
	miner.extract_last_commits(session, 'v1.5.0')

	repo2 = Repository('repo/projectforge')
	sys2 = System('ProjectForge', repo2)

	miner = RepositoryMiner(repo2, sys2)	
	miner.add_ignore_dir_with('test')		
	miner.extract_last_commits(session, '6.25.0-RELEASE')
	
	ecosystem = Ecosystem()

	ecolyzer = EcosystemAnalyzer(ecosystem)
	ecolyzer.make_relations(sys2, sys1, session)

	relationships = ecosystem.relationships

	assert len(relationships) == 9

	rel1 = relationships[0]
	rel2 = relationships[8]

	assert rel1.from_system.name == 'ProjectForge'
	assert rel1.from_author.name == 'Florian Blumenstein'
	assert rel1.from_author.email == 'f.blumenstein@micromata.de'
	assert rel1.to_system.name == 'JFreeChart'
	assert rel1.to_author.name == 'David Gilbert'	
	assert rel1.to_author.email == 'dave@jfree.org'	
	assert rel1.from_code_element.name == rel1.to_code_element.name == 'getDayOfMonth'
	assert rel1.from_code_element_count == 2
	
	assert rel2.from_system.name == 'ProjectForge'
	assert rel2.from_author.name == 'Florian Blumenstein'
	assert rel2.from_author.email == 'f.blumenstein@micromata.de'	
	assert rel2.to_system.name == 'JFreeChart'
	assert rel2.to_author.name == 'David Gilbert'	
	assert rel2.to_author.email == 'dave@jfree.org'	
	assert rel2.from_code_element.name == rel2.to_code_element.name == 'addSeries'	
	assert rel2.from_code_element_count == 6

	session.close()
	db.drop_all()	