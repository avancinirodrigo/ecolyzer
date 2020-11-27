from ecolyzer.ecosystem import EcosystemAnalyzer
from ecolyzer.system import System, File, SourceFile, Operation, Call
from ecolyzer.repository import Repository, Person, Author, GitPython
from ecolyzer.ecosystem import Ecosystem

def test_make_relations(mocker):
	mocker.patch.object(GitPython, 'IsGitRepo', return_value=True)
	mocker.patch.object(GitPython, 'CurrentBranch', return_value='master')
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

	mocker.patch.object(EcosystemAnalyzer, '_total_of_calls', return_value=10)

	ecolyzer = EcosystemAnalyzer(ecosystem)
	ecolyzer.make_relations(sys2, sys1)

	relationships = ecosystem.relationships

	assert len(relationships) == 2

	rel1 = relationships[0]
	rel2 = relationships[1]

	assert rel1.from_system.name == 'ca'
	assert rel1.from_author.name == 'CA Dev'
	assert rel1.from_author.email == 'ca.dev@ca.com'
	assert rel1.to_system.name == 'terrame'
	assert rel1.to_author.name == 'TerraMe Dev'	
	assert rel1.to_author.email == 'tme.dev@terrame.com'	
	assert rel1.from_code_element.name == rel1.to_code_element.name == 'Cell'
	
	assert rel2.from_system.name == 'ca'
	assert rel2.from_author.name == 'CA Dev'
	assert rel2.from_author.email == 'ca.dev@ca.com'	
	assert rel2.to_system.name == 'terrame'
	assert rel2.to_author.name == 'TerraMe Dev'	
	assert rel2.to_author.email == 'tme.dev@terrame.com'	
	assert rel2.from_code_element.name == rel2.to_code_element.name == 'CellularSpace'	
