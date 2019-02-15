from ecolyzer.repository import File
from ecolyzer.dataaccess import SQLAlchemyEngine

db_url = 'postgresql://postgres:postgres@localhost:5432/file_test'
db = SQLAlchemyEngine(db_url)
db.create_all(True)

def test_file_crud():
	#create
	filepath = 'some/path/file.ext'
	file = File(filepath)
	assert file.name == 'file'
	assert file.path == 'some/path'
	assert file.ext == 'ext'
	assert file.fullpath() == filepath

	session = db.create_session()	
	session.add(file)
	session.commit()

	#read	
	filedb = session.query(File).get(1)
	assert filedb.name == file.name
	assert filedb.path == file.path
	assert filedb.ext == file.ext
	assert filedb.fullpath() == file.fullpath()

	#update
	file.name = 'renamed_file'
	assert file.fullpath() == 'some/path/renamed_file.ext'
	session.commit()	
	filedb = session.query(File).get(1)
	assert filedb.fullpath() == file.fullpath()

	#delete
	session.delete(file)
	session.commit()
	filedb = session.query(File).get(1)
	assert filedb == None

	session.close()
	db.drop_all()
	