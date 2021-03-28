from ecolyzer.repository import Repository, Author, Person
from ecolyzer.system import System, File, SourceFile, Operation, Call
from ecolyzer.dataaccess import SQLAlchemyORM
from ecolyzer.ecosystem import Relationship, RelationInfo, FromRelationInfo, Ecosystem


def test_add_relationship(mocker):
	db_url = 'postgresql://postgres:postgres@localhost:5432/eco_add_relation'
	db = SQLAlchemyORM(db_url)
	db.create_all(True)	

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
	c21 = Call('get', src2)	
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
	mocker.patch.object(c21, 'author', return_value=ca_author, autospec=True)	

	to_info = RelationInfo(sys1, src1, c11)
	from_info = FromRelationInfo(sys2, src2, f21, 10)
	rel1 = Relationship(from_info, to_info)

	to_info = RelationInfo(sys1, src1, f11)
	from_info = FromRelationInfo(sys2, src2, c21, 20)
	rel2 = Relationship(from_info, to_info)

	eco = Ecosystem()
	eco.add_relationship(rel1)
	eco.add_relationship(rel2)

	session.add(eco)
	session.commit()
	ecodb = session.query(Ecosystem).one()
	relsdb = ecodb.relationships

	assert len(relsdb) == 2
	
	rel1db = relsdb[0]
	assert rel1db.from_system.name == 'ca'
	assert rel1db.to_system.name == 'terrame'
	assert rel1db.from_source_file.name == 'file2'
	assert rel1db.to_source_file.name == 'file1'
	assert rel1db.from_code_element.name == 'call'
	assert rel1db.to_code_element.name == 'call'
	assert rel1db.from_author.name == 'CA Dev'
	assert rel1db.to_author.name == 'TerraMe Dev'
	assert rel1db.from_code_element_count == 10

	rel2db = relsdb[1]
	assert rel2db.from_system.name == 'ca'
	assert rel2db.to_system.name == 'terrame'
	assert rel2db.from_source_file.name == 'file2'
	assert rel2db.to_source_file.name == 'file1'
	assert rel2db.from_code_element.name == 'get'
	assert rel2db.to_code_element.name == 'get'
	assert rel2db.from_author.name == 'CA Dev'
	assert rel2db.to_author.name == 'TerraMe Dev'
	assert rel2db.from_code_element_count == 20

	session.close()
	db.drop_all()	
