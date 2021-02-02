from ecolyzer.dataaccess import SQLAlchemyORM
from ecolyzer.ucs import MappingEcosystemDependents
from ecolyzer.ecosystem import Ecosystem


def test_uc():	
	db_url = 'postgresql://postgres:postgres@localhost:5432/scribejava_ecosystem'
	db = SQLAlchemyORM(db_url)
	db.create_all(True)	

	repo_url = 'https://github.com/scribejava/scribejava'
	uc = MappingEcosystemDependents(repo_url, branch='master', ecosystem_name='ScribeJava',
		ignore_dirs_with=['test', 'scribejava-apis', 'scribejava-httpclient'])
	session = db.create_session()
	uc.execute(session)

	ecosystem = session.query(Ecosystem).\
			filter(Ecosystem.name == 'ScribeJava').first()
	assert len(ecosystem.relationships) >= 37

	session.close()
	db.drop_all()


def test_repo_exists():
	db_url = 'postgresql://postgres:postgres@localhost:5432/scribejava_ecosystem_exists'
	db = SQLAlchemyORM(db_url)
	db.create_all(True)	

	repo_url = 'https://github.com/scribejava/scribejava'
	uc = MappingEcosystemDependents(repo_url, branch='master', ecosystem_name='ScribeJava',
		ignore_dirs_with=['test', 'scribejava-apis', 'scribejava-httpclient'], stars=1)
	session = db.create_session()
	uc.execute(session)

	del session

	uc = MappingEcosystemDependents(repo_url, branch='master', ecosystem_name='ScribeJava',
		ignore_dirs_with=['test', 'scribejava-apis', 'scribejava-httpclient'])
	session = db.create_session()
	uc.execute(session)	

	ecosystem = session.query(Ecosystem).\
			filter(Ecosystem.name == 'ScribeJava').first()
	assert len(ecosystem.relationships) >= 37	

	session.close()	
	db.drop_all()


def test_no_relationships():	
	db_url = 'postgresql://postgres:postgres@localhost:5432/scribejava_ecosystem'
	db = SQLAlchemyORM(db_url)
	db.create_all(True)	

	repo_url = 'https://github.com/scribejava/scribejava'
	uc = MappingEcosystemDependents(repo_url, branch='master', ecosystem_name='ScribeJava',
		ignore_dirs_with=['test', 'scribejava-apis', 'scribejava-httpclient'], forks=1000)
	session = db.create_session()
	uc.execute(session)

	ecosystem = session.query(Ecosystem).\
			filter(Ecosystem.name == 'ScribeJava').first()
	assert len(ecosystem.relationships) == 0

	session.close()
	db.drop_all()	