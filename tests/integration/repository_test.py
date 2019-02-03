from ecolyzer.repository import Repository
from ecolyzer.system import System
from ecolyzer.dataaccess import SQLAlchemyEngine

db_url = 'postgresql://postgres:postgres@localhost:5432/repo_test'
SQLAlchemyEngine().create_all(db_url, True)

def test_repository_create():
	repo = Repository('repo/terrame')
	sys1 = System('terrame', repo)
	session = SQLAlchemyEngine().create_session()	
	session.add(repo)
	session.add(sys1)
	session.commit()
	repodb = session.query(Repository).get(1)
	sys1db = session.query(System).get(1)
	assert repo.path == repodb.path	
	assert sys1db.repo_id == repodb.id
	#sys2 = System('ca', repo) < TODO: review
	#session.add(sys2)
	session.commit()	
	session.close()
	SQLAlchemyEngine().drop_all(db_url)
	