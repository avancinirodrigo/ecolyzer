from ecolyzer.repository import File
from ecolyzer.system import SourceFile, Function
from ecolyzer.dataaccess import SQLAlchemyEngine

db_url = 'postgresql://postgres:postgres@localhost:5432/function_test'

def test_function_crud():
	db = SQLAlchemyEngine(db_url)
	db.create_all(True)

	#create
	filepath = 'some/path/file.src'
	file = File(filepath)
	src_file = SourceFile(file)
	f1 = Function('get', src_file)
	f2 = Function('add', src_file)

	session = db.create_session()
	session.add(src_file)
	session.commit()

	#read
	funcsdb = session.query(Function).all()
	assert len(funcsdb) == 2
	assert funcsdb[0].name == 'get'
	assert funcsdb[1].name == 'add'
	
	# update
	f1.name = 'getX'
	session.commit()
	f1db = session.query(Function).get(1)
	assert f1db.name == 'getX'
	
	#delete
	session.delete(f1)
	session.commit()
	funcsdb = session.query(Function).all()
	assert len(funcsdb) == 1
	session.delete(f2)
	funcsdb = session.query(Function).all()
	assert len(funcsdb) == 0
	filedb = session.query(File).get(1)
	src_filedb = session.query(SourceFile).get(1)
	assert filedb.name == 'file'	
	assert src_filedb.ext == 'src'
	
	session.close()
	db.drop_all()