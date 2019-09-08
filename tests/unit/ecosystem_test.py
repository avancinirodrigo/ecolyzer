from ecolyzer.system import System, File, SourceFile, Operation, Call
from ecolyzer.repository import Repository, Person, Author, GitPython
from ecolyzer.ecosystem import Ecosystem, RelationInfo, Relationship

def test_add_same_relation(mocker):
	mocker.patch.object(GitPython, 'IsGitRepo', return_value=True)
	repo1 = Repository('some/path/terrame')
	sys1 = System('terrame', repo1)
	f1 = File('Cell.lua')
	src1 = SourceFile(f1)
	op1 = Operation('Cell', src1)
	src1.add_code_element(op1)

	f2 = File('CellularSpace.lua')	
	src2 = SourceFile(f2)
	op2 = Operation('CellularSpace', src2)
	src2.add_code_element(op2)	

	sys1.add_source_file(src1)
	sys1.add_source_file(src2)

	repo2 = Repository('some/path/ca')
	sys2 = System('ca', repo2)
	f3 = File('Anneal.lua')
	src3 = SourceFile(f3)
	c1 = Call('Cell', src3)
	src3.add_code_element(c1)
	c2 = Call('CellularSpace', src3)
	src3.add_code_element(c2)

	sys2.add_source_file(src3)	

	ecosystem = Ecosystem()

	tme_author = Author(Person('TerraMe Dev', 'tme.dev@terrame.com'))
	ca_author = Author(Person('CA Dev', 'ca.dev@ca.com'))
	mocker.patch.object(op1, 'author', return_value=tme_author, autospec=True)
	mocker.patch.object(op2, 'author', return_value=tme_author, autospec=True)
	mocker.patch.object(c1, 'author', return_value=ca_author, autospec=True)
	mocker.patch.object(c2, 'author', return_value=ca_author, autospec=True)	

	to_info = RelationInfo(sys1, src1, op1)
	from_info = RelationInfo(sys2, src3, c1)

	rel1 = Relationship(from_info, to_info)
	rel2 = Relationship(from_info, to_info)

	assert rel1.from_system == rel2.from_system
	assert rel1.to_system == rel2.to_system
	assert rel1.from_code_element == rel2.from_code_element
	assert rel1.to_code_element == rel2.to_code_element	

	ecosystem.add_relationship(rel1)
	ecosystem.add_relationship(rel2)

	assert len(ecosystem.relationships()) == 2
	ecosystem.relationships()[0] = rel1
	ecosystem.relationships()[1] = rel2
