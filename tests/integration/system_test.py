from ecolyzer.system import System
from ecolyzer.dataaccess import SQLAlchemyEngine

db_url = 'postgresql://postgres:postgres@localhost:5432/system_test'
SQLAlchemyEngine().createdb(db_url, True)
SQLAlchemyEngine().create_engine(db_url)
SQLAlchemyEngine().create_all_tables()

def test_system_create():
	session = SQLAlchemyEngine().create_session()
	sys = System('terrame')
	session.add(sys)
	session.commit()	
	sysdb = session.query(System).get(1)
	assert sys.name == sysdb.name
	session.close()
	SQLAlchemyEngine().dropdb(db_url)
	