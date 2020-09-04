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
			filter(Ecosystem.name=='ScribeJava').first()
	assert len(ecosystem.relationships) >= 43

	session.commit()
	session.close()