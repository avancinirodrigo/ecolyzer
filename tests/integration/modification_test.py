import datetime
from ecolyzer.system import File, System
from ecolyzer.repository import Repository, Commit, CommitInfo, Person, Author, Modification, ModificationInfo
from ecolyzer.dataaccess import SQLAlchemyORM

db_url = 'postgresql://postgres:postgres@localhost:5432/modific_test'
db = SQLAlchemyORM(db_url)
db.create_all(True)

def test_crud():
	#create
	repo = Repository('repo/terrame')
	sys = System('terrame', repo)
	commit_info = CommitInfo('hashhashhash')
	commit_info.date = datetime.datetime(2019, 2, 6, 14, 14, 55)  
	commit_info.msg = 'commit message'
	commit_info.author_name = 'author'
	commit_info.author_email = 'author@email.com'	
	author = Author(Person(commit_info.author_name, commit_info.author_email))
	commit = Commit(commit_info, author, repo)
	modinfo = ModificationInfo('some/path/file.ext')
	modinfo.old_path = ''
	modinfo.new_path = 'some/path/file.ext'
	modinfo.added = 10
	modinfo.removed = 0
	modinfo.status = 'ADD'
	file = File(modinfo.filename)
	mod = Modification(modinfo, file, commit)
	
	session = db.create_session()
	session.add(mod)
	session.commit()

	#read	
	moddb = session.query(Modification).get(1)
	assert moddb.new_path == 'some/path/file.ext'
	assert moddb.old_path == ''
	assert moddb.added == 10
	assert moddb.removed == 0
	assert moddb.status == 'ADD'
	assert moddb.commit_id == 1
	assert moddb.file_id == 1

	#update
	mod.status = 'DELETED'
	session.commit()	
	moddb = session.query(Modification).get(1)
	assert moddb.status == 'DELETED'

	#delete
	session.delete(mod)
	session.commit()
	moddb = session.query(Modification).get(1)
	commitdb = session.query(Commit).get(1)
	repodb = session.query(Repository).get(1)
	authordb = session.query(Author).get(1)
	filedb = session.query(File).get(1)
	assert moddb == None
	assert commitdb.id == 1
	assert repodb.id == 1 
	assert authordb.id == 1
	assert filedb.id == 1


	session.close()
	db.drop_all()
	