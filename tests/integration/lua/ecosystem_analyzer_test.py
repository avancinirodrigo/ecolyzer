from ecolyzer.ecosystem import EcosystemAnalyzer
from ecolyzer.system import System
from ecolyzer.repository import Repository, Person, Author, RepositoryMiner, GitPython
from ecolyzer.dataaccess import SQLAlchemyORM
from ecolyzer.ecosystem import Ecosystem

def test_make_relations():
	db_url = 'postgresql://postgres:postgres@localhost:5432/ecolyzer_relations'
	db = SQLAlchemyORM(db_url)
	db.create_all(True)
	session = db.create_session()

	repo1 = Repository('repo/terrame')
	sys1 = System('terrame', repo1)

	session.add(repo1)
	session.add(sys1)

	miner = RepositoryMiner(repo1, sys1)
	git = GitPython(repo1.path)
	hashs1 = git.commit_hashs_reverse(10)
	for hash in hashs1:
		miner.extract(session, hash)

	repo2 = Repository('repo/ca')
	sys2 = System('ca', repo2)

	miner = RepositoryMiner(repo2, sys2)
	git = GitPython(repo2.path)
	hashs2 = git.commit_hashs_reverse(10)
	for hash in hashs2:
		miner.extract(session, hash)
	
	ecosystem = Ecosystem()

	ecolyzer = EcosystemAnalyzer(ecosystem)
	ecolyzer.make_relations(sys2, sys1, session)

	relationships = ecosystem.relationships

	assert len(relationships) == 292

	rel1 = relationships[0]
	rel2 = relationships[291]

	assert rel1.from_system.name == 'ca'
	assert rel1.from_author.name == 'Pedro Andrade'
	assert rel1.from_author.email == 'pedro.andrade@inpe.br'
	assert rel1.to_system.name == 'terrame'
	assert rel1.to_author.name == 'rvmaretto'	
	assert rel1.to_author.email == 'rvmaretto@gmail.com'	
	assert rel1.from_code_element.name == rel1.to_code_element.name == 'notify'
	assert rel1.from_code_element_count == 1
	
	assert rel2.from_system.name == 'ca'
	assert rel2.from_author.name == 'Pedro Andrade'
	assert rel2.from_author.email == 'pedro.andrade@inpe.br'	
	assert rel2.to_system.name == 'terrame'
	assert rel2.to_author.name == 'rvmaretto'	
	assert rel2.to_author.email == 'rvmaretto@gmail.com'	
	assert rel2.from_code_element.name == rel2.to_code_element.name == 'type'
	assert rel2.from_code_element_count == 1

	session.close()
	db.drop_all()

def test_relations_last_commits():
	db_url = 'postgresql://postgres:postgres@localhost:5432/ecolyzer_relations_last'
	db = SQLAlchemyORM(db_url)
	db.create_all(True)
	session = db.create_session()

	repo1 = Repository('repo/terrame')
	sys1 = System('terrame', repo1)

	session.add(repo1)
	session.add(sys1)

	miner = RepositoryMiner(repo1, sys1)
	miner.add_ignore_dir_with('test')
	miner.add_ignore_dir_with('example')	
	miner.extract_last_commits(session, '2.0-RC-8')

	repo2 = Repository('repo/ca')
	sys2 = System('ca', repo2)

	miner = RepositoryMiner(repo2, sys2)	
	miner.extract_last_commits(session)
	
	ecosystem = Ecosystem()

	ecolyzer = EcosystemAnalyzer(ecosystem)
	ecolyzer.make_relations(sys2, sys1, session)

	relationships = ecosystem.relationships

	assert len(relationships) == 531

	rel1 = relationships[0]
	rel2 = relationships[530]

	assert rel1.from_system.name == 'ca'
	assert rel1.from_author.name == 'Pedro Andrade'
	assert rel1.from_author.email == 'pedro.andrade@inpe.br'
	assert rel1.to_system.name == 'terrame'
	assert rel1.to_author.name == 'wsenafranca'	
	assert rel1.to_author.email == 'wsenafranca@gmail.com'	
	assert rel1.from_code_element.name == rel1.to_code_element.name == 'run'
	assert rel1.from_code_element_count == 1
	
	assert rel2.from_system.name == 'ca'
	assert rel2.from_author.name == 'Pedro Andrade'
	assert rel2.from_author.email == 'pedro.andrade@inpe.br'	
	assert rel2.to_system.name == 'terrame'
	assert rel2.to_author.name == 'Pedro Andrade'	
	assert rel2.to_author.email == 'pedro.andrade@inpe.br'	
	assert rel2.from_code_element.name == rel2.to_code_element.name == 'assertSnapshot'	
	assert rel2.from_code_element_count == 1

	session.close()
	db.drop_all()	