from ecolyzer.system import System, File, SourceFile
from ecolyzer.repository import Repository
from ecolyzer.dataaccess import SQLAlchemyORM

def test_system_crud():
	db_url = 'postgresql://postgres:postgres@localhost:5432/system_crud'
	db = SQLAlchemyORM(db_url)
	db.create_all(True)	

	#create
	repo = Repository('repo/terrame')
	sys = System('terrame', repo)

	session = db.create_session()	
	session.add(repo)
	session.add(sys)
	session.commit()

	#read	
	sysdb = session.query(System).get(1)
	assert sys.name == sysdb.name
	assert sys.repository.path == sysdb.repository.path

	#update
	sys.name = 'TerraME-2.0'
	session.commit()	
	sysdb = session.query(System).get(1)
	assert sysdb.name == sys.name

	#delete
	session.delete(sys)
	session.commit()
	sysdb = session.query(System).get(1)
	repodb = session.query(Repository).get(1)
	assert sysdb == None
	assert repodb.path == repo.path 

	session.close()
	db.drop_all()
	
def test_add_file():
	db_url = 'postgresql://postgres:postgres@localhost:5432/system_add_file'
	db = SQLAlchemyORM(db_url)
	db.create_all(True)

	repo = Repository('repo/terrame')
	sys = System('terrame', repo)

	session = db.create_session()	
	session.add(repo)
	session.add(sys)

	file1 = File('path/file1.ext')
	sys.add_file(file1)

	session.commit()

	sysdb = session.query(System).get(1)
	file1db = sysdb.get_file(file1.fullpath)
	assert file1db.fullpath == file1.fullpath 

	session.close()
	db.drop_all()

def test_add_source_file():
	db_url = 'postgresql://postgres:postgres@localhost:5432/sys_add_src_file'
	db = SQLAlchemyORM(db_url)
	db.create_all(True)

	repo = Repository('repo/terrame')
	sys = System('terrame', repo)

	session = db.create_session()	
	session.add(repo)
	session.add(sys)

	file1 = File('path/file1.ext')
	src1 = SourceFile(file1)
	sys.add_source_file(src1)

	session.commit()

	sysdb = session.query(System).get(1)
	src1db = sysdb.get_source_file(file1.fullpath)
	assert src1db.file.fullpath == src1.file.fullpath 
	assert src1db.ext() == src1.file.ext

	session.close()
	db.drop_all()	