from ecolyzer.repository import Repository
from ecolyzer.system import File, SourceFile, Operation
from ecolyzer.dataaccess import SQLAlchemyORM

def test_operation_crud():
	db_url = 'postgresql://postgres:postgres@localhost:5432/operation_crud'
	db = SQLAlchemyORM(db_url)
	db.create_all(True)

	#create
	filepath = 'some/path/file.src'
	file = File(filepath)
	src_file = SourceFile(file)
	f1 = Operation('get', src_file)
	f2 = Operation('add', src_file)

	session = db.create_session()
	session.add(src_file)
	session.commit()

	#read
	funcsdb = session.query(Operation).all()
	assert len(funcsdb) == 2
	assert funcsdb[0].name == 'get'
	assert funcsdb[1].name == 'add'
	
	# update
	f1.name = 'getX'
	session.commit()
	f1db = session.query(Operation).get(1)
	assert f1db.name == 'getX'
	
	#delete
	session.delete(f1)
	session.commit()
	funcsdb = session.query(Operation).all()
	assert len(funcsdb) == 1
	session.delete(f2)
	session.commit()
	funcsdb = session.query(Operation).all()
	assert len(funcsdb) == 0
	filedb = session.query(File).get(1)
	src_filedb = session.query(SourceFile).get(1)
	assert filedb.name == 'file'	
	assert src_filedb.ext() == 'src'
	
	session.close()
	db.drop_all()
	
def test_add_operation_same_name():
	db_url = 'postgresql://postgres:postgres@localhost:5432/function_same_name'
	db = SQLAlchemyORM(db_url)
	db.create_all(True)
 
	file1 = File('some/path/file1.src')
	src_file1 = SourceFile(file1)
	f1 = Operation('get', src_file1)
	
	file2 = File('some/path/file2.src')
	src_file2 = SourceFile(file2)
	f2 = Operation('get', src_file2)

	session = db.create_session()
	#session.add(src_file1)
	#session.add(src_file2)
	session.commit()
	
	session.close()
	db.drop_all()	