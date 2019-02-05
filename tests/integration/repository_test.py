from ecolyzer.repository import Repository
from ecolyzer.system import System
from ecolyzer.dataaccess import SQLAlchemyEngine

db_url = 'postgresql://postgres:postgres@localhost:5432/repo_test'
db = SQLAlchemyEngine(db_url)
db.create_all(True)

def test_repository_crud():
	#create
	repo = Repository('repo/terrame')
	sys = System('terrame', repo)
	session = db.create_session()	
	session.add(repo)
	session.add(sys)
	session.commit()

	#read
	repodb = session.query(Repository).get(1)
	sysdb = session.query(System).get(1)
	assert repo.path == repodb.path	
	assert sysdb.repo_id == repodb.id
	#sys2 = System('ca', repo) < TODO: review
	#session.add(sys2)

	# update
	repo.path = 'repo/ca'
	session.commit()	
	repodb = session.query(Repository).get(1)
	assert repo.path == repodb.path	
	assert sysdb.repo_id == repodb.id

	#delete
	session.delete(repo)
	session.commit()
	repodb = session.query(Repository).get(1)
	sysdb = session.query(System).get(1)
	assert repodb == None
	assert sysdb == None

	session.close()
	db.drop_all()
	