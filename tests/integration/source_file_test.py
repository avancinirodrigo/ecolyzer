import pytest
from ecolyzer.repository import Repository
from ecolyzer.system import File, SourceFile, Operation, Call
from ecolyzer.dataaccess import SQLAlchemyORM

def test_source_file_crud():
	db_url = 'postgresql://postgres:postgres@localhost:5432/src_file_crud'
	db = SQLAlchemyORM(db_url)
	db.create_all(True)

	#create
	filepath = 'some/path/file.src'
	file = File(filepath)
	src_file = SourceFile(file)
	f1 = Operation('get', src_file)
	f2 = Operation('add', src_file)
	c1 = Call('call', src_file)	
	src_file.add_code_element(f1)
	src_file.add_code_element(f2)
	src_file.add_code_element(c1)

	session = db.create_session()
	session.add(file)
	session.commit()

	#read
	src_filedb = session.query(SourceFile).get(1)
	assert src_filedb.file_id == file.id
	assert src_filedb.file.ext == file.ext
	assert src_filedb.code_element_by_key(f1.key)
	assert src_filedb.code_element_by_key(f2.key)
	assert src_filedb.code_element_by_key(c1.key)

	#update
	file.ext = 'crs'
	f3 = Operation('update', src_file)
	session.add(f3)
	session.commit()
	src_filedb = session.query(SourceFile).get(1)
	code_elements = session.query(Operation).filter_by(source_file_id = src_filedb.id).all()	
	assert src_filedb.file.ext == file.ext
	assert len(code_elements) == 3

	#delete
	session.delete(src_file)
	session.commit()
	src_filedb = session.query(SourceFile).get(1)
	filedb = session.query(File).get(1)
	funcsdb = session.query(Operation).all()
	assert src_filedb == None
	assert filedb.name == 'file'
	assert len(funcsdb) == 0

	session.close()
	db.drop_all()

def test_one_to_one_relation():
	db_url = 'postgresql://postgres:postgres@localhost:5432/src_file_one_to_one'	
	db = SQLAlchemyORM(db_url)
	db.create_all(True)
	
	filepath = 'some/path/file.src'
	file = File(filepath)
	src_file1 = SourceFile(file)
	#src_file2 = SourceFile(file) #TODO(#42): how to test one-to-one relationship
	
	session = db.create_session()
	session.add(src_file1)
	#session.add(src_file2)
	session.commit()
	
	src_filedb1 = session.query(SourceFile).get(1)
	src_filedb2 = session.query(SourceFile).get(2)
	assert src_file1.file_id == 1
	#assert src_file2.file_id == 1 #TODO: one to one seems not working
	
	session.close()
	db.drop_all()

def test_add_operation():
	db_url = 'postgresql://postgres:postgres@localhost:5432/src_file_one_to_one'	
	db = SQLAlchemyORM(db_url)
	db.create_all(True)

	filepath = 'some/path/file.src'
	file = File(filepath)
	src_file = SourceFile(file)

	f1 = Operation('get', src_file)
	src_file.add_code_element(f1)

	session = db.create_session()
	session.add(src_file)
	session.commit()	

	f1db = session.query(Operation).get(1)
	assert f1db.name == 'get'
	assert f1db.source_file_id == 1

	session.close()
	db.drop_all()	 

def test_add_same_code_element():
	db_url = 'postgresql://postgres:postgres@localhost:5432/src_add_same'	
	db = SQLAlchemyORM(db_url)
	db.create_all(True)

	filepath = 'some/path/file.src'
	file = File(filepath)
	src_file = SourceFile(file)

	f1 = Operation('get', src_file)
	src_file.add_code_element(f1)

	session = db.create_session()
	session.add(src_file)
	session.commit()	

	src_filedb = session.query(SourceFile).one()
	f2 = Operation('get', src_filedb)

	with pytest.raises(Exception) as e:
		src_filedb.add_code_element(f2)
	assert (('Code element \'get\' of type \'Operation\' is already present')
			in str(e.value))
	session.close()
	db.drop_all()	 	