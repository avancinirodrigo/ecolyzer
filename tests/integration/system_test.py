from ecolyzer.system import System
from ecolyzer.repository import Repository
from ecolyzer.dataaccess import SQLAlchemyEngine

db_url = 'postgresql://postgres:postgres@localhost:5432/system_test'
db = SQLAlchemyEngine(db_url)
db.create_all(True)

def test_system_crud():
	#create
	repo = Repository('repo/terrame')
	sys = System('terrame', repo)
	session = db.create_session()	
	session.add(repo)
	session.add(sys)
	session.commit()

	#read	
	sysdb = session.query(System).get(1)
	assert sys.name == sysdb.name
	assert sys.repository.path == sysdb.repository.path

	#update
	sys.name = 'TerraME-2.0'
	session.commit()	
	sysdb = session.query(System).get(1)
	assert sysdb.name == sys.name

	#delete
	session.delete(sys)
	session.commit()
	sysdb = session.query(System).get(1)
	repodb = session.query(Repository).get(1)
	assert sysdb == None
	assert repodb.path == repo.path 

	session.close()
	db.drop_all()
	