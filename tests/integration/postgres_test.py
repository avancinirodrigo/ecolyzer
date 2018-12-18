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

def test_dropdb_dbopened():
	Postgres().connect('postgres')
	dbname = 'drop_opened_db'
	Postgres().dropdb(dbname)
	Postgres().createdb(dbname)
	Postgres().close()
	Postgres().connect(dbname)
	with pytest.raises(Exception) as e:
		Postgres().dropdb(dbname)
	assert (('Error while dropping database: '
			+ 'cannot drop the currently open database\n.')
			in str(e.value))
	Postgres().close()
	Postgres().connect('postgres')
	Postgres().dropdb(dbname)
	Postgres().close()

def test_create_release_table():
	Postgres().connect('postgres')
	dbname = 'release_test'
	Postgres().dropdb(dbname)
	Postgres().createdb(dbname)
	Postgres().close()
	Postgres().connect(dbname)
	Postgres().create_release_table()
	assert Postgres().table_exists('release')
	Postgres().close()
	Postgres().connect('postgres')
	Postgres().dropdb(dbname)
	Postgres().close()

def test_create_source_file_db():
	Postgres().connect('postgres')
	dbname = 'source_file_test'
	Postgres().dropdb(dbname)
	Postgres().createdb(dbname)
	Postgres().close()
	Postgres().connect(dbname)
	Postgres().create_source_file_table()
	assert Postgres().table_exists('source_file')
	Postgres().close()
	Postgres().connect('postgres')
	Postgres().dropdb(dbname)
	Postgres().close()

def test_insert_into_release_table():
	Postgres().connect('postgres')
	dbname = 'insert_into_release'
	Postgres().dropdb(dbname)
	Postgres().createdb(dbname)
	Postgres().close()
	Postgres().connect(dbname)
	Postgres().create_release_table()
	Postgres().insert_into_release_table(0, "rc1")
	rels = Postgres().select_from('release')
	# change to dictCursor https://wiki.postgresql.org/wiki/Psycopg2_Tutorial
	assert rels[0][0] == 0
	assert rels[0][1] == 'rc1'
	Postgres().close()
	Postgres().connect('postgres')
	Postgres().dropdb(dbname)
	Postgres().close()
