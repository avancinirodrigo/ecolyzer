from ecolyzer.repository import File
from ecolyzer.system import SourceFile
from ecolyzer.dataaccess import SQLAlchemyEngine

db_url = 'postgresql://postgres:postgres@localhost:5432/src_file_test'
db = SQLAlchemyEngine(db_url)
db.create_all(True)

def test_source_file_crud():
	#create
	filepath = 'some/path/file.src'
	file = File(filepath)
	src_file = SourceFile(file)

	session = db.create_session()
	session.add(file)
	session.commit()

	#read
	src_filedb = session.query(SourceFile).get(1)
	assert src_filedb.file_id == file.id
	assert src_filedb.ext == file.ext

	#update
	file.ext = 'crs'
	src_file.ext = 'crs' #TODO: HOW UPDATE WHEN FILE UPDATE
	session.commit()
	src_filedb = session.query(SourceFile).get(1)
	assert src_filedb.ext == file.ext

	# #delete
	# session.delete(file)
	# session.commit()
	# filedb = session.query(File).get(1)
	# assert filedb == None

	session.close()
	#db.drop_all()
