import pytest

from gitdriller import Postgres

def test_connect():
	assert Postgres().connect('postgres')
	Postgres().close()

def test_connect_exception():
	with pytest.raises(Exception) as e:
		Postgres().connect('pos')
	assert (('Connection not established FATAL:  '
			+ 'database "pos" does not exist\n')
			in str(e.value))

def test_createdb():
	Postgres().connect('postgres')
	Postgres().dropdb('pythondb')
	assert Postgres().createdb('pythondb')
	Postgres().dropdb('pythondb')
	Postgres().close()

def test_createdb_exception():
	Postgres().connect('postgres')
	Postgres().createdb('pythondb')
	with pytest.raises(Exception) as e:
		Postgres().createdb('pythondb')
	assert (('Error while creating database: '
			+ 'database "pythondb" already exists\n.')
			in str(e.value))
	Postgres().dropdb('pythondb')
	Postgres().close()

def test_existsdb():
	Postgres().connect('postgres')
	assert Postgres().existsdb('postgres')
	assert not Postgres().existsdb('pppp')
	Postgres().close()

def test_dropdb():
	Postgres().connect('postgres')
	assert not Postgres().dropdb('pythondb')
	Postgres().createdb('pythondb')
	assert Postgres().dropdb('pythondb')
	Postgres().close()
