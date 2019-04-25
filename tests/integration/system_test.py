from ecolyzer.system import System, File
from ecolyzer.repository import Repository
from ecolyzer.dataaccess import SQLAlchemyEngine

def test_system_crud():
	db_url = 'postgresql://postgres:postgres@localhost:5432/system_crud'
	db = SQLAlchemyEngine(db_url)
	db.create_all(True)	

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
	
def test_add_file():
	db_url = 'postgresql://postgres:postgres@localhost:5432/system_add_file'
	db = SQLAlchemyEngine(db_url)
	db.create_all(True)

	repo = Repository('repo/terrame')
	sys = System('terrame', repo)
	session = db.create_session()	
	session.add(repo)
	session.add(sys)

	file1 = File('path/file1.ext')
	sys.add_file(file1)

	session.commit()

	file1db = session.query(File).get(1)	
	assert file1db.system_id == sys.id

	session.close()
	db.drop_all()
