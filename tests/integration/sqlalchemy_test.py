import pytest
from ecolyzer.dataaccess import SQLAlchemyORM

def test_createdb():
	url = 'postgresql://postgres:postgres@localhost:5432/createdb'
	db = SQLAlchemyORM(url)
	db.createdb(True)
	assert db.existsdb()
	db.dropdb()
	assert not db.existsdb()

def test_createdb_dbexists():
	url = 'postgresql://postgres:postgres@localhost:5432/createdb'
	db = SQLAlchemyORM(url)
	db.createdb(True)
	with pytest.raises(Exception) as e:
		db.createdb(False)
	assert (('Database \'createdb\' already exists.')
			in str(e.value))
	db.dropdb()

def test_overwrite():
	url = 'postgresql://postgres:postgres@localhost:5432/overwritedb'
	db = SQLAlchemyORM(url)
	db.createdb()
	assert db.existsdb()
	db.createdb(True)
	assert db.existsdb()
	db.dropdb()	
