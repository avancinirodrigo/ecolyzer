from ecolyzer.system import System
from ecolyzer.repository import Repository
from ecolyzer.dataaccess import SQLAlchemyEngine

db_url = 'postgresql://postgres:postgres@localhost:5432/system_test'
SQLAlchemyEngine().create_all(db_url, True)

def test_system_create():
	repo = Repository('repo/terrame')
	sys = System('terrame', repo)
	session = SQLAlchemyEngine().create_session()	
	session.add(repo)
	session.add(sys)
	session.commit()	
	sysdb = session.query(System).get(1)
	assert sys.name == sysdb.name
	assert sys.repository.path == sysdb.repository.path
	session.close()
	SQLAlchemyEngine().drop_all(db_url)
	