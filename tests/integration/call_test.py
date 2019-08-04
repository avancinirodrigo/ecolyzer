from ecolyzer.repository import Repository
from ecolyzer.system import File, SourceFile, Call
from ecolyzer.dataaccess import SQLAlchemyORM

def test_call_crud():
	db_url = 'postgresql://postgres:postgres@localhost:5432/call_crud'
	db = SQLAlchemyORM(db_url)
	db.create_all(True)

	#create
	filepath = 'some/path/file.src'
	file = File(filepath)
	src_file = SourceFile(file)
	f1 = Call('get', src_file)
	f2 = Call('add', src_file)

	session = db.create_session()
	session.add(src_file)
	session.commit()

	#read
	funcsdb = session.query(Call).all()
	assert len(funcsdb) == 2
	assert funcsdb[0].name == 'get'
	assert funcsdb[0].type == 'call'
	assert funcsdb[1].name == 'add'
	
	# update
	f1.name = 'getX'
	session.commit()
	f1db = session.query(Call).get(1)
	assert f1db.name == 'getX'
	
	#delete
	session.delete(f1)
	session.commit()
	funcsdb = session.query(Call).all()
	assert len(funcsdb) == 1
	session.delete(f2)
	funcsdb = session.query(Call).all()
	assert len(funcsdb) == 0
	filedb = session.query(File).get(1)
	src_filedb = session.query(SourceFile).get(1)
	assert filedb.name == 'file'	
	assert src_filedb.ext() == 'src'
	
	session.close()
	db.drop_all()
	