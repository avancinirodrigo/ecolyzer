from ecolyzer.repository import Repository
from ecolyzer.system import File, SourceFile, Operation, Call
from ecolyzer.dataaccess import SQLAlchemyORM
from ecolyzer.ecosystem import Relationship

def test_crud():
	db_url = 'postgresql://postgres:postgres@localhost:5432/relation_crud'
	db = SQLAlchemyORM(db_url)
	db.create_all(True)	

	#create
	f1 = File('some/path/file1.src')
	src1 = SourceFile(f1)
	f11 = Operation('get', src1)
	f12 = Operation('add', src1)
	c11 = Call('call', src1)	
	src1.add_code_element(f11)
	src1.add_code_element(f12)
	src1.add_code_element(c11)

	f2 = File('some/path/file2.src')
	src2 = SourceFile(f2)
	f21 = Operation('call', src2)	
	src2.add_code_element(f21)	

	session = db.create_session()
	session.add(src1)
	session.add(src2)
	session.commit()

	rel = Relationship(src1.id, src2.id, 'code')
	session.add(rel)
	session.commit()

	session.close()
	#db.drop_all()	
