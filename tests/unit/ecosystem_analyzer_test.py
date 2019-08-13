from ecolyzer.ecosystem import EcosystemAnalyzer
from ecolyzer.system import System, File, SourceFile, Operation, Call
from ecolyzer.repository import Repository
from ecolyzer.ecosystem import Ecosystem

def test_make_relations():
	repo1 = Repository('repo/terrame')
	sys1 = System('terrame', repo1)
	f1 = File('Cell.lua')
	src1 = SourceFile(f1)
	op1 = Operation('Cell')
	src1.add_code_element(op1)

	f2 = File('CellularSpace.lua')	
	src2 = SourceFile(f2)
	op2 = Operation('CellularSpace')
	src2.add_code_element(op2)	

	sys1.add_source_file(src1)
	sys1.add_source_file(src2)

	repo2 = Repository('repo/ca')
	sys2 = System('ca', repo2)
	f3 = File('Anneal.lua')
	src3 = SourceFile(f3)
	c1 = Call('Cell')
	src3.add_code_element(c1)
	c2 = Call('CellularSpace')
	src3.add_code_element(c2)

	sys2.add_source_file(src3)	

	ecosystem = Ecosystem()

	ecolyzer = EcosystemAnalyzer(ecosystem)
	ecolyzer.make_relations(sys1, sys2)

	relationships = ecosystem.relationships()

	assert len(relationships) == 2

	rel1 = relationships[0]
	rel2 = relationships[1]

	#print(rel1.__dict__)
	assert rel1.from_system.name == 'ca'
	assert rel1.to_system.name == 'terrame'
