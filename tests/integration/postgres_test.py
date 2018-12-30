import pytest

from gitdriller import Postgres, GitFile

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

def test_create_tag_table():
	Postgres().connect('postgres')
	dbname = 'tag_test'
	Postgres().dropdb(dbname)
	Postgres().createdb(dbname)
	Postgres().close()
	Postgres().connect(dbname)
	Postgres().create_tag_table()
	assert Postgres().table_exists('tag')
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

def test_insert_into_tag_table():
	Postgres().connect('postgres')
	dbname = 'insert_into_tag'
	Postgres().dropdb(dbname)
	Postgres().createdb(dbname)
	Postgres().close()
	Postgres().connect(dbname)
	Postgres().create_tag_table()
	Postgres().insert_into_tag_table(0, "rc1")
	rels = Postgres().select_from('tag')
	assert rels[0].id == 0
	assert rels[0].name == 'rc1'
	Postgres().insert_into_tag_table(1, "rc2")
	rels = Postgres().select_from('tag')
	assert rels[0].id == 0
	assert rels[0].name == 'rc1'
	assert rels[1].id == 1
	assert rels[1].name == 'rc2'
	Postgres().close()
	Postgres().connect('postgres')
	Postgres().dropdb(dbname)
	Postgres().close()

def test_insert_into_src_table():
	Postgres().connect('postgres')
	dbname = 'insert_into_src'
	Postgres().dropdb(dbname)
	Postgres().createdb(dbname)
	Postgres().close()
	Postgres().connect(dbname)
	Postgres().create_source_file_table()
	src1 = GitFile('some/path/file1.ext')
	src1.added = 10
	Postgres().insert_into_source_file_table(0, src1, 0)
	src = Postgres().select_from('source_file')
	assert src[0].id == 0
	assert src[0].path == src1.fullpath
	assert src[0].added_lines == src1.added
	assert src[0].ext == src1.ext
	assert src[0].tagid == 0
	src2 = GitFile('other/path/file2.txe')
	src2.added = 20
	Postgres().insert_into_source_file_table(1, src2, 1)
	src = Postgres().select_from('source_file')
	assert src[0].id == 0
	assert src[0].path == src1.fullpath
	assert src[0].added_lines == src1.added
	assert src[0].ext == src1.ext
	assert src[0].tagid == 0
	assert src[1].id == 1
	assert src[1].path == src2.fullpath
	assert src[1].added_lines == src2.added
	assert src[1].ext == src2.ext
	assert src[1].tagid == 1
	Postgres().close()
	Postgres().connect('postgres')
	Postgres().dropdb(dbname)
	Postgres().close()