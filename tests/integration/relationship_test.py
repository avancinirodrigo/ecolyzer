from ecolyzer.repository import Repository, Author, Person
from ecolyzer.system import System, File, SourceFile, Operation, Call
from ecolyzer.dataaccess import SQLAlchemyORM
from ecolyzer.ecosystem import Relationship, RelationInfo, FromRelationInfo

def test_crud(mocker):
	db_url = 'postgresql://postgres:postgres@localhost:5432/relation_crud'
	db = SQLAlchemyORM(db_url)
	db.create_all(True)	

	#create
	repo1 = Repository('repo/terrame')
	sys1 = System('terrame', repo1)	
	f1 = File('some/path/file1.src')
	src1 = SourceFile(f1)
	f11 = Operation('get', src1)
	f12 = Operation('add', src1)
	c11 = Call('call', src1)	
	src1.add_code_element(f11)
	src1.add_code_element(f12)
	src1.add_code_element(c11)
	sys1.add_source_file(src1)

	repo2 = Repository('repo/ca')
	sys2 = System('ca', repo2)
	f2 = File('some/path/file2.src')
	src2 = SourceFile(f2)
	f21 = Operation('call', src2)	
	src2.add_code_element(f21)
	sys2.add_source_file(src2)	

	session = db.create_session()
	session.add(src1)
	session.add(src2)
	session.commit()

	tme_author = Author(Person('TerraMe Dev', 'tme.dev@terrame.com'))
	ca_author = Author(Person('CA Dev', 'ca.dev@ca.com'))
	mocker.patch.object(f11, 'author', return_value=tme_author, autospec=True)
	mocker.patch.object(f12, 'author', return_value=tme_author, autospec=True)
	mocker.patch.object(c11, 'author', return_value=tme_author, autospec=True)
	mocker.patch.object(f21, 'author', return_value=ca_author, autospec=True)	

	to_info = RelationInfo(sys1, src1, c11)
	from_info = FromRelationInfo(sys2, src2, f21, 10)

	rel = Relationship(from_info, to_info)
	session.add(rel)
	session.commit()

	relsdb = session.query(Relationship).all()

	assert len(relsdb) == 1

	reldb = relsdb[0]
	assert reldb.from_system.name == 'ca'
	assert reldb.to_system.name == 'terrame'
	assert reldb.from_source_file.name() == 'file2'
	assert reldb.to_source_file.name() == 'file1'
	assert reldb.from_code_element.name == 'call'
	assert reldb.to_code_element.name == 'call'
	assert reldb.from_author.name == 'CA Dev'
	assert reldb.to_author.name == 'TerraMe Dev'
	assert reldb.from_code_element_count == 10

	session.close()
	db.drop_all()	
