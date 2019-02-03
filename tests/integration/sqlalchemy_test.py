import pytest
from ecolyzer.dataaccess import SQLAlchemyEngine

def test_createdb():
	url = 'postgresql://postgres:postgres@localhost:5432/createdb'
	SQLAlchemyEngine().createdb(url, True)
	assert SQLAlchemyEngine().existsdb(url)
	SQLAlchemyEngine().dropdb(url)
	assert not SQLAlchemyEngine().existsdb(url)

def test_createdb_dbexists():
	url = 'postgresql://postgres:postgres@localhost:5432/createdb'
	SQLAlchemyEngine().createdb(url, True)
	with pytest.raises(Exception) as e:
		SQLAlchemyEngine().createdb(url, False)
	assert (('Database \'createdb\' already exists.')
			in str(e.value))
	SQLAlchemyEngine().dropdb(url)
