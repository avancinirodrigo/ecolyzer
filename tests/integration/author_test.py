from ecolyzer.repository import Repository, Author, Person
from ecolyzer.dataaccess import SQLAlchemyEngine

def test_crud():
	db_url = 'postgresql://postgres:postgres@localhost:5432/author_crud'
	db = SQLAlchemyEngine(db_url)
	db.create_all(True)

	#create
	repo = Repository('repo/terrame')
	person = Person('dev1', 'dev1@email.com')
	author = Author(person, repo)

	session = db.create_session()
	session.add(author)
	session.commit()

	authordb = session.query(Author).one()
	assert authordb.person == person
	assert authordb.repository == repo

	session.close()	
	db.drop_all()

def test_same_person_in_two_repos():
	db_url = 'postgresql://postgres:postgres@localhost:5432/author_two_repos'
	db = SQLAlchemyEngine(db_url)
	db.create_all(True)

	repo1 = Repository('repo/terrame')
	person = Person('dev1', 'dev1@email.com')
	author1 = Author(person, repo1)

	repo2 = Repository('repo/ca')
	author2 = Author(person, repo2)

	session = db.create_session()
	session.add(author1)
	session.commit()

	authorsdb = session.query(Author).all()

	assert len(authorsdb) == 2
	assert authorsdb[0].person == authorsdb[1].person
	assert authorsdb[0].repository != authorsdb[1].repository

	session.close()	
	db.drop_all()

def test_delete_cascade():
	db_url = 'postgresql://postgres:postgres@localhost:5432/author_del_cascade'
	db = SQLAlchemyEngine(db_url)
	db.create_all(True)

	repo1 = Repository('repo/terrame')
	person = Person('dev1', 'dev1@email.com')
	author1 = Author(person, repo1)

	repo2 = Repository('repo/ca')
	author2 = Author(person, repo2)

	session = db.create_session()
	session.add(author1)
	session.commit()

	authorsdb = session.query(Author).all()
	
	assert len(authorsdb) == 2

	session.delete(person)
	session.commit()

	authorsdb = session.query(Author).all()

	assert len(authorsdb) == 0

	session.close()	
	db.drop_all()	
