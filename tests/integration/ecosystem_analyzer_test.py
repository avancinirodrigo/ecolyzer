from ecolyzer.ecosystem import EcosystemAnalyzer
from ecolyzer.system import System
from ecolyzer.repository import Repository, Person, Author, RepositoryMiner, Git
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
	git = Git(repo1.path)
	hashs1 = git.commit_hashs_reverse(10)
	for hash in hashs1:
		miner.extract(session, hash)

	repo2 = Repository('repo/ca')
	sys2 = System('ca', repo2)

	miner = RepositoryMiner(repo2, sys2)
	git = Git(repo2.path)
	hashs2 = git.commit_hashs_reverse(10)
	for hash in hashs2:
		miner.extract(session, hash)
	
	ecosystem = Ecosystem()

	ecolyzer = EcosystemAnalyzer(ecosystem)
	ecolyzer.make_relations(sys2, sys1, session)

	relationships = ecosystem.relationships()

	for rel in relationships:
		assert rel.from_code_element.name == rel.to_code_element.name
		print(rel.from_code_element.name)
		print(rel.from_system.name, rel.from_code_element.source_file.name())
		print(rel.to_system.name, rel.to_code_element.source_file.name())
		print("")

	# assert len(relationships) == 2

	# rel1 = relationships[0]
	# rel2 = relationships[1]

	# assert rel1.from_system.name == 'ca'
	# assert rel1.from_author.name == 'CA Dev'
	# assert rel1.from_author.email == 'ca.dev@ca.com'
	# assert rel1.to_system.name == 'terrame'
	# assert rel1.to_author.name == 'TerraMe Dev'	
	# assert rel1.to_author.email == 'tme.dev@terrame.com'	
	# assert rel1.from_code_element.name == rel1.to_code_element.name == 'Cell'
	
	# assert rel2.from_system.name == 'ca'
	# assert rel2.from_author.name == 'CA Dev'
	# assert rel2.from_author.email == 'ca.dev@ca.com'	
	# assert rel2.to_system.name == 'terrame'
	# assert rel2.to_author.name == 'TerraMe Dev'	
	# assert rel2.to_author.email == 'tme.dev@terrame.com'	
	# assert rel2.from_code_element.name == rel2.to_code_element.name == 'CellularSpace'	
	
	session.close()