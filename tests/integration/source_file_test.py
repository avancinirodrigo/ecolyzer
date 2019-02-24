from ecolyzer.system import File, SourceFile, Function
from ecolyzer.dataaccess import SQLAlchemyEngine

db_url = 'postgresql://postgres:postgres@localhost:5432/src_file_test'

def test_source_file_crud():
	db = SQLAlchemyEngine(db_url)
	db.create_all(True)

	#create
	filepath = 'some/path/file.src'
	file = File(filepath)
	src_file = SourceFile(file)
	f1 = Function('get', src_file)
	f2 = Function('add', src_file)	

	session = db.create_session()
	session.add(file)
	session.commit()

	#read
	src_filedb = session.query(SourceFile).get(1)
	assert src_filedb.file_id == file.id
	assert src_filedb.ext == file.ext

	#update
	file.ext = 'crs'
	src_file.ext = 'crs'
	session.commit()
	src_filedb = session.query(SourceFile).get(1)
	assert src_filedb.ext == file.ext

	#delete
	session.delete(src_file)
	session.commit()
	src_filedb = session.query(SourceFile).get(1)
	filedb = session.query(File).get(1)
	funcsdb = session.query(Function).all()
	assert src_filedb == None
	assert filedb.name == 'file'
	assert len(funcsdb) == 0

	session.close()
	db.drop_all()

def test_one_to_one_relation():
	db = SQLAlchemyEngine(db_url)
	db.create_all(True)
	
	filepath = 'some/path/file.src'
	file = File(filepath)
	src_file1 = SourceFile(file)
	src_file2 = SourceFile(file)
	
	session = db.create_session()
	session.add(src_file1)
	session.add(src_file2)
	session.commit()
	
	src_filedb1 = session.query(SourceFile).get(1)
	src_filedb2 = session.query(SourceFile).get(2)
	assert src_file1.file_id == 1
	assert src_file2.file_id == 1 #TODO: one to one seems not working
	
	session.close()
	db.drop_all()
