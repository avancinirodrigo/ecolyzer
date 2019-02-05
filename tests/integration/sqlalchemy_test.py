import pytest
from ecolyzer.dataaccess import SQLAlchemyEngine

def test_createdb():
	url = 'postgresql://postgres:postgres@localhost:5432/createdb'
	db = SQLAlchemyEngine(url)
	db.createdb(True)
	assert db.existsdb()
	db.dropdb()
	assert not db.existsdb()

def test_createdb_dbexists():
	url = 'postgresql://postgres:postgres@localhost:5432/createdb'
	db = SQLAlchemyEngine(url)
	db.createdb(True)
	with pytest.raises(Exception) as e:
		db.createdb(False)
	assert (('Database \'createdb\' already exists.')
			in str(e.value))
	db.dropdb()
