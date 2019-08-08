from ecolyzer.repository import Repository, Author, Person
from ecolyzer.system import System
from ecolyzer.dataaccess import SQLAlchemyORM

def test_repository_crud():
	db_url = 'postgresql://postgres:postgres@localhost:5432/repo_crud'
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
	repodb = session.query(Repository).get(1)
	sysdb = session.query(System).get(1)
	assert repo.path == repodb.path	
	assert sysdb.repo_id == repodb.id
	#sys2 = System('ca', repo) < TODO: review
	#session.add(sys2)

	# update
	repo.path = 'repo/ca'
	session.commit()	
	repodb = session.query(Repository).get(1)
	assert repo.path == repodb.path	
	assert sysdb.repo_id == repodb.id

	#delete
	session.delete(repo)
	session.commit()
	repodb = session.query(Repository).get(1)
	sysdb = session.query(System).get(1)
	assert repodb == None
	assert sysdb == None

	session.close()
	db.drop_all()
	
def test_two_repos():
	db_url = 'postgresql://postgres:postgres@localhost:5432/repo_two_repos'
	db = SQLAlchemyORM(db_url)
	db.create_all(True)

	repo1 = Repository('repo/terrame')
	sys1 = System('terrame', repo1)

	repo2 = Repository('repo/ca')
	sys2 = System('ca', repo2)

	session = db.create_session()	
	session.add(sys1)
	session.add(sys2)
	session.commit()

	sys1db = session.query(System).filter_by(name = sys1.name).one()
	sys2db = session.query(System).filter_by(name = sys2.name).one()

	assert sys1db.name == sys1.name
	assert sys1db.repository.path == repo1.path 
	assert sys2db.name == sys2.name
	assert sys2db.repository.path == repo2.path
	assert sys1db.name != sys2db.name

	session.close()
	db.drop_all()

def test_authors():
	db_url = 'postgresql://postgres:postgres@localhost:5432/repo_authors'
	db = SQLAlchemyORM(db_url)
	db.create_all(True)

	repo = Repository('repo/terrame')
	sys = System('terrame', repo)
	dev1 = Author(Person('dev1', 'dev1@mail.com'))
	repo.add_author(dev1)
	
	assert repo.author_exists(dev1.email)

	session = db.create_session()
	session.add(repo)
	session.commit()
	repodb = session.query(Repository).get(1)

	assert repodb.author_exists(dev1.email)

	session.close()
	db.drop_all()		

def test_same_author_in_two_repo():
	db_url = 'postgresql://postgres:postgres@localhost:5432/repo_author_intwo'
	db = SQLAlchemyORM(db_url)
	db.create_all(True)

	repo1 = Repository('repo/terrame')
	sys1 = System('terrame', repo1)
	person = Person('dev1', 'dev1@mail.com') 
	dev1 = Author(person)
	repo1.add_author(dev1)

	session = db.create_session()
	session.add(repo1)	
	session.commit()

	repo2 = Repository('repo/ca')
	sys2 = System('ca', repo2)
	
	persondb = session.query(Person).get(1)

	assert persondb.email == dev1.email

	repo2.add_author(Author(persondb))

	session.add(repo2)
	session.commit()	

	authorsdb = session.query(Author).all()

	assert len(authorsdb) == 2
	assert authorsdb[0].email == authorsdb[1].email 
	assert authorsdb[0].repository != authorsdb[1].repository
	assert authorsdb[0].repository_id == repo1.id 
	assert authorsdb[1].repository_id == repo2.id 

	session.close()
	db.drop_all()
