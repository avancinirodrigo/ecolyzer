import datetime
from ecolyzer.system import File
from ecolyzer.repository import (Repository, Commit, CommitInfo,
								Author, Person, Modification, 
								ModificationInfo)
from ecolyzer.dataaccess import SQLAlchemyORM

db_url = 'postgresql://postgres:postgres@localhost:5432/commit_test'
db = SQLAlchemyORM(db_url)
db.create_all(True)


def test_crud():
	# create
	repo = Repository('repo/terrame')
	# sys = System('terrame', repo)
	commit_info = CommitInfo('hashhashhash')
	commit_info.date = datetime.datetime(2019, 2, 6, 14, 14, 55)  
	commit_info.msg = 'commit message'
	commit_info.author_name = 'author'
	commit_info.author_email = 'author@email.com'	
	author = Author(Person(commit_info.author_name, commit_info.author_email), repo)
	commit = Commit(commit_info, author, repo)
	modinfo = ModificationInfo('some/path/file.ext')
	modinfo.old_path = ''
	modinfo.new_path = 'some/path/file.ext'
	modinfo.added = 10
	modinfo.removed = 0
	modinfo.type = 'ADD'
	file = File(modinfo.filename)
	mod = Modification(modinfo, file, commit)	

	assert mod.id is None
	
	session = db.create_session()
	session.add(commit)
	session.commit()

	assert mod.id is not None

	# read	
	commitdb = session.query(Commit).get(1)
	assert commitdb.msg == commit_info.msg
	assert commitdb.date.strftime('%Y-%m-%d %H:%M:%S') == '2019-02-06 14:14:55'
	assert commitdb.hash == commit_info.hash
	assert commitdb.repository.path == repo.path
	assert commitdb.author.name == commit_info.author_name
	assert commitdb.author.email == commit_info.author_email

	# update
	commit.msg = 'updating message'
	session.commit()	
	commitdb = session.query(Commit).get(1)
	assert commitdb.msg == commit.msg

	# delete
	session.delete(commit)
	session.commit()
	commitdb = session.query(Commit).get(1)
	moddb = session.query(Modification).get(1)
	repodb = session.query(Repository).get(1)
	authordb = session.query(Author).get(1)
	filedb = session.query(File).get(1)
	assert commitdb is None
	assert moddb is None
	assert repodb.path == repo.path 
	assert authordb.email == author.email
	assert filedb.id == 1 == file.id

	session.close()
	db.drop_all()
