from ecolyzer.system import System
from ecolyzer.repository import Repository
from ecolyzer.dataaccess import SQLAlchemyORM
from ecolyzer.ecosystem import CentralSystem


def test_crud():
	db_url = 'postgresql://postgres:postgres@localhost:5432/central_system_crud'
	db = SQLAlchemyORM(db_url)
	db.create_all(True)	

	# create
	repo = Repository('repo/terrame')
	sys = System('terrame', repo)
	central = CentralSystem(sys)

	session = db.create_session()	
	session.add(central)
	session.commit()

	session.close()
	db.drop_all()	
