import os
from ecolyzer.repository import RepositoryMiner, Repository, CommitInfo, Commit, Author, Modification
from ecolyzer.system import System, File, SourceFile, Operation, Call
from ecolyzer.dataaccess import SQLAlchemyEngine
	
def test_get_commit():
	db_url = 'postgresql://postgres:postgres@localhost:5432/miner_get_commit'
	db = SQLAlchemyEngine(db_url)
	db.create_all(True)
	repo = Repository('repo/terrame')
	sys = System('terrame', repo)
	miner = RepositoryMiner(repo, sys)
	commit_info = miner.get_commit_info('80a562be869dbb984229f608ae9a04d05c5e1689')

	assert commit_info.msg == 'Initial commit'
	assert commit_info.date.strftime('%Y-%m-%d %H:%M:%S') == '2014-09-15 08:12:11'
	assert commit_info.hash == '80a562be869dbb984229f608ae9a04d05c5e1689'
	assert commit_info.author_name == 'pedro-andrade-inpe'
	assert commit_info.author_email == 'pedro.andrade@inpe.br'
	assert len(commit_info.modifications) == 1
	assert commit_info.modifications[0].filename == 'LICENSE'
	assert commit_info.modifications[0].old_path == None
	assert commit_info.modifications[0].new_path == 'LICENSE'
	assert commit_info.modifications[0].added == 674
	assert commit_info.modifications[0].removed == 0
	assert commit_info.modifications[0].status == 'ADD'

	author = Author(commit_info.author_name, commit_info.author_email)
	commit = Commit(commit_info, author, repo)
	fmodinfo = commit_info.modifications[0]
	file = File(fmodinfo.filename)
	filemod = Modification(fmodinfo, file, commit)
	session = db.create_session()
	session.add(repo)
	session.add(sys)
	session.add(commit)
	session.add(file)
	session.add(filemod)
	session.commit()

	filemoddb = session.query(Modification).get(1)
	commitdb = filemoddb.commit
	filedb = filemoddb.file

	assert commitdb.msg == 'Initial commit'
	assert commitdb.date.strftime('%Y-%m-%d %H:%M:%S') == '2014-09-15 08:12:11'
	assert commitdb.hash == '80a562be869dbb984229f608ae9a04d05c5e1689'
	assert commitdb.repository.path == repo.path
	assert commitdb.author.name == 'pedro-andrade-inpe'
	assert commitdb.author.email == 'pedro.andrade@inpe.br'	
	assert filedb.fullpath == 'LICENSE'
	assert filemoddb.old_path == None
	assert filemoddb.new_path == 'LICENSE'
	assert filemoddb.added == 674
	assert filemoddb.removed == 0
	assert filemoddb.status == 'ADD'

	commit_info = miner.get_commit_info('ffb8347b2de44eb05f6c5eba3b3cb8b7716acebb')

	assert commit_info.msg == 'Delete LICENSE'
	assert commit_info.date.strftime('%Y-%m-%d %H:%M:%S') == '2014-09-17 11:49:45'
	assert commit_info.hash == 'ffb8347b2de44eb05f6c5eba3b3cb8b7716acebb'
	assert commit_info.author_name == 'pedro-andrade-inpe'
	assert commit_info.author_email == 'pedro.andrade@inpe.br'
	assert len(commit_info.modifications) == 1
	assert commit_info.modifications[0].filename == 'LICENSE'
	assert commit_info.modifications[0].old_path == 'LICENSE'
	assert commit_info.modifications[0].new_path == None
	assert commit_info.modifications[0].added == 0
	assert commit_info.modifications[0].removed == 674	
	assert commit_info.modifications[0].status == 'DELETE'

	commit = Commit(commit_info, author, repo)
	fmodinfo = commit_info.modifications[0]
	filemod = Modification(fmodinfo, file, commit)
	session.add(commit)
	session.add(filemod)
	session.commit()
	
	filemoddb2 = session.query(Modification).get(2)
	commitdb2 = filemoddb2.commit
	filedb2 = filemoddb2.file

	assert commitdb2.msg == 'Delete LICENSE'
	assert commitdb2.date.strftime('%Y-%m-%d %H:%M:%S') == '2014-09-17 11:49:45'
	assert commitdb2.hash == 'ffb8347b2de44eb05f6c5eba3b3cb8b7716acebb'
	assert commitdb2.repository.id == repo.id
	assert commitdb2.author.name == 'pedro-andrade-inpe'
	assert commitdb2.author.email == 'pedro.andrade@inpe.br'		
	assert filedb2.fullpath == 'LICENSE'
	assert filemoddb2.old_path == 'LICENSE'
	assert filemoddb2.new_path == None
	assert filemoddb2.added == 0
	assert filemoddb2.removed == 674
	assert filemoddb2.status == 'DELETE'	

	filemoddb1 = session.query(Modification).get(1)
	commitdb1 = filemoddb1.commit
	filedb1 = filemoddb1.file

	assert commitdb1.msg == 'Initial commit'
	assert commitdb1.date.strftime('%Y-%m-%d %H:%M:%S') == '2014-09-15 08:12:11'
	assert commitdb1.hash == '80a562be869dbb984229f608ae9a04d05c5e1689'
	assert commitdb1.repository.path == repo.path	
	assert commitdb2.author.name == 'pedro-andrade-inpe'
	assert commitdb2.author.email == 'pedro.andrade@inpe.br'
	assert filedb1.fullpath == 'LICENSE'
	assert filemoddb1.old_path == None
	assert filemoddb1.new_path == 'LICENSE'
	assert filemoddb1.added == 674
	assert filemoddb1.removed == 0
	assert filemoddb1.status == 'ADD'	

	session.close()
	db.drop_all()
	
def test_extract():
	db_url = 'postgresql://postgres:postgres@localhost:5432/miner_extract'
	db = SQLAlchemyEngine(db_url)
	db.create_all(True)
	repo = Repository('repo/terrame')
	sys = System('terrame', repo)
	session = db.create_session()
	session.add(repo)
	session.add(sys)
	session.commit()
	miner = RepositoryMiner(repo, sys)
	miner.extract(session, '082dff5e822ea1b4491911b7bf434a7f47a4be26')
	filedb = session.query(File).filter_by(fullpath = 'base/lua/CellularSpace.lua').first()
	srcfiledb = session.query(SourceFile).filter_by(file_id = filedb.id).first()
	commitdb = session.query(Commit).filter(Commit.hash == '082dff5e822ea1b4491911b7bf434a7f47a4be26').one()
	assert commitdb.msg == ('* New structure for directories.\n'
							'* Function require already implemented.\n'
							'* Function -config-tests already moved to terrame.lua and working.\n'
							'* Function -test already moved to terrame.lua, but still having problems when executing the tests.')
	authordb = session.query(Author).filter(Author.id == commitdb.author_id).one()
	assert authordb.name == 'rvmaretto'
	modificationsdb = session.query(Modification).filter_by(commit_id = commitdb.id).all()

	files_mod = {
		'base/description.lua' : True,
		'base/load.lua' : True,
		'base/lua/Action.lua' : True,
		'base/lua/Agent.lua' : True,
		'base/lua/Automaton.lua' : True,
		'base/lua/Cell.lua' : True,
		'base/lua/CellularSpace.lua' : True,
		'base/lua/Coord.lua' : True,
		'base/lua/Environment.lua' : True,
		'base/lua/Event.lua' : True,
		'base/lua/Flow.lua' : True,
		'base/lua/Group.lua' : True,
		'base/lua/Jump.lua' : True,
		'base/lua/Legend.lua' : True,
		'base/lua/Model.lua' : True,
		'base/lua/Neighborhood.lua' : True,
		'base/lua/Observer.lua' : True,
		'base/lua/Pair.lua' : True,
		'base/lua/Random.lua' : True,
		'base/lua/SocialNetwork.lua' : True,
		'base/lua/Society.lua' : True,
		'base/lua/State.lua' : True,
		'base/lua/Timer.lua' : True,
		'base/lua/Trajectory.lua' : True,
		'base/lua/UnitTest.lua' : True,
		'base/lua/Utils.lua' : True,
		'base/tests/core/alternative/Agent.lua' : True,
		'base/tests/core/alternative/Automaton.lua' : True,
		'base/tests/core/alternative/Cell.lua' : True,
		'base/tests/core/alternative/CellularSpace.lua' : True,
		'base/tests/core/alternative/Coord.lua' : True,
		'base/tests/core/alternative/Environment.lua' : True,
		'base/tests/core/alternative/Event.lua' : True,
		'base/tests/core/alternative/Flow.lua' : True,
		'base/tests/core/alternative/Group.lua' : True,
		'base/tests/core/alternative/Jump.lua' : True,
		'base/tests/core/alternative/Model.lua' : True,
		'base/tests/core/alternative/Neighborhood.lua' : True,
		'base/tests/core/alternative/Random.lua' : True,
		'base/tests/core/alternative/SocialNetwork.lua' : True,
		'base/tests/core/alternative/Society.lua' : True,
		'base/tests/core/alternative/State.lua' : True,
		'base/tests/core/alternative/Timer.lua' : True,
		'base/tests/core/alternative/Trajectory.lua' : True,
		'base/tests/core/alternative/Utils.lua' : True,
		'base/tests/core/basics/Agent.lua' : True,
		'base/tests/core/basics/Cell.lua' : True,
		'base/tests/core/basics/CellularSpace.lua' : True,
		'base/tests/core/basics/Coord.lua' : True,
		'base/tests/core/basics/Environment.lua' : True,
		'base/tests/core/basics/Event.lua' : True,
		'base/tests/core/basics/Group.lua' : True,
		'base/tests/core/basics/Jump.lua' : True,
		'base/tests/core/basics/Memory.lua' : True,
		'base/tests/core/basics/Model.lua' : True,
		'base/tests/core/basics/Neighborhood.lua' : True,
		'base/tests/core/basics/Random.lua' : True,
		'base/tests/core/basics/SocialNetwork.lua' : True,
		'base/tests/core/basics/Society.lua' : True,
		'base/tests/core/basics/Timer.lua' : True,
		'base/tests/core/basics/Trajectory.lua' : True,
		'base/tests/core/basics/Utils.lua' : True,
		'src/lua/terrame.lua' : True	
	}

	for mod in modificationsdb:
		assert files_mod[mod.new_path]

	operationsdb = session.query(Operation).filter_by(source_file_id = srcfiledb.id).all()

	operations = {
		'CellularSpace' : True,
		'coordCoupling' : True,
		'createMooreNeighborhood' : True,
		'createVonNeumannNeighborhood' : True,
		'createNeighborhood' : True,
		'createMxNNeighborhood' : True,
		'spatialCoupling' : True,
		'add' : True,
		'getCell' : True,
		'get' : True,
		'getCells' : True,
		'getCellByID' : True,
		'load' : True,
		'loadShape' : True,
		'loadNeighborhood' : True,
		'notify' : True,
		'sample' : True,
		'save' : True,
		'saveShape' : True,
		'size' : True,
		'split' : True,
		'synchronize' : True,
		'moore' : True,
		'mxn' : True,
		'vonneumann' : True,
		'coord' : True,
		'__len' : True	
	}

	for op in operationsdb:
		assert operations[op.name]

	calls = {
		'addNeighborhood' : True,
		'addCell' : True,
		'getNeighborhood' : True,
		'caseof' : True,
		'clear' : True,
		'endswith' : True,
		'getTime' : True,
		'integer' : True,
		'getDBName' : True,
		'sub' : True,
		'setDBType' : True,
		'setDBName' : True,
		'len' : True,
		'setPort' : True,
		'setHostName' : True,
		'setUser' : True,
		'setPassword' : True,
		'setTheme' : True,
		'setLayer' : True,
		'setWhereClause' : True,
		'clearAttrName' : True,
		'addAttrName' : True,
		'setReference' : True,
		'getLayerName' : True,
		'init' : True,
		'forEachCell' : True,
		'Neighborhood' : True,
		'ipairs' : True,
		'weightF' : True,
		'filterF' : True,
		'customWarningMsg' : True,
		'namedParametersErrorMsg' : True,
		'type' : True,
		'defaultValueWarningMsg' : True,
		'incompatibleTypesErrorMsg' : True,
		'checkUnnecessaryParameters' : True,
		'mandatoryArgumentErrorMsg' : True,
		'incompatibleValuesErrorMsg' : True,
		'switch' : True,
		'deprecatedFunctionWarningMsg' : True,
		'Coord' : True,
		'readCSV' : True,
		'tostring' : True,
		'Cell' : True,
		'customErrorMsg' : True,
		'pairs' : True,
		'tableParameterErrorMsg' : True,
		'resourceNotFoundErrorMsg' : True,
		'print' : True,
		'argument' : True,
		'Trajectory' : True,
		'getn' : True,
		'TeCellularSpace' : True,
		'incompatibleFileExtensionErrorMsg' : True,
		'setmetatable' : True,
		'forEachElement' : True
	}

	callsdb = session.query(Call).filter_by(source_file_id = srcfiledb.id).all()	
	
	for call in callsdb:
		assert calls[call.name]

	session.close()
	db.drop_all()

def test_get_commit_source_file():
	db_url = 'postgresql://postgres:postgres@localhost:5432/miner_sources'
	db = SQLAlchemyEngine(db_url)
	db.create_all(True)
	repo = Repository('repo/terrame')
	sys = System('terrame', repo)
	miner = RepositoryMiner(repo, sys)
	commit_info = miner.get_commit_info('082dff5e822ea1b4491911b7bf434a7f47a4be26')
	author = Author(commit_info.author_name, commit_info.author_email)
	commit = Commit(commit_info, author, repo)
	session = db.create_session()
	for mod_info in commit_info.modifications:
		file = File(mod_info.new_path)
		sys.add_file(file)
		mod = Modification(mod_info, file, commit)
		if miner.is_source_file(file):
			srcfile = SourceFile(file)
			code_elements = miner.extract_code_elements(srcfile, mod)
			for element in code_elements:
			 	element.modification = mod
			 	session.add(element)		
			session.add(mod)			

	session.commit()
	afile = sys.get_file('base/lua/CellularSpace.lua')
	srcfiledb = session.query(SourceFile).filter_by(file_id = afile.id).first()
	assert srcfiledb.file.ext == 'lua'
	assert srcfiledb.file.name == 'CellularSpace'
	#TODO: how to load all functions together?
	#assert len(srcfiledb.functions) == 1

	moddb = session.query(Modification).filter_by(file_id = afile.id).first()
	asrc_file = SourceFile(afile)
	assert asrc_file.code_elements_len() == 0

	#miner.extract_code_elements(asrc_file, moddb)
	#assert len(asrc_file.operations) == 1
	#assert asrc_file.operation_exists('CellularSpace')

	functions = session.query(Operation).filter_by(source_file_id = srcfiledb.id).all()	
	#assert asrc_file.operation_exists(functions[0].name)
	assert functions[0].name == 'CellularSpace'

	session.close()
	db.drop_all()

def test_extract_tag_interval():
	db_url = 'postgresql://postgres:postgres@localhost:5432/miner_tag_interval'
	db = SQLAlchemyEngine(db_url)
	db.create_all(True)
	repo = Repository('repo/terrame')
	sys = System('terrame', repo)
	session = db.create_session()
	session.add(repo)
	session.add(sys)
	session.commit()
	miner = RepositoryMiner(repo, sys)
	#miner.commit_interval('80a562be869dbb984229f608ae9a04d05c5e1689', 
	#					'082dff5e822ea1b4491911b7bf434a7f47a4be26') TODO: not working
	miner.tag_interval('2.0-RC-6', '2.0-RC-7')
	miner.extract(session)

	commits = session.query(Commit).all()

	assert len(commits) == 95

	session.close()
	db.drop_all()	

def test_extract_deleted_files():
	db_url = 'postgresql://postgres:postgres@localhost:5432/miner_del_files'
	db = SQLAlchemyEngine(db_url)
	db.create_all(True)
	repo = Repository('repo/terrame')
	sys = System('terrame', repo)
	session = db.create_session()
	session.add(repo)
	session.add(sys)
	session.commit()
	miner = RepositoryMiner(repo, sys)

	miner.extract(session, '082dff5e822ea1b4491911b7bf434a7f47a4be26')
	file = session.query(File).filter_by(fullpath = 'src/lua/terrame.lua').one()
	mod = session.query(Modification).filter_by(file_id = file.id).first()

	assert mod.new_path == 'src/lua/terrame.lua'
	assert mod.old_path == None
	assert mod.status == 'ADD'
	assert sys.file_exists('src/lua/terrame.lua')

	miner.extract(session, 'f2e117598feee9db8cabbd1c300e143199e12d92')	
	file = session.query(File).filter_by(fullpath = 'src/lua/terrame.lua').one()
	mod = session.query(Modification).filter_by(file_id = file.id).filter_by(status = 'DELETE').first()
	
	assert mod.new_path == None
	assert mod.old_path == 'src/lua/terrame.lua'	
	assert mod.status == 'DELETE'
	assert sys.file_exists('src/lua/terrame.lua')

	session.close()
	db.drop_all()

def test_extract_renamed_files():
	db_url = 'postgresql://postgres:postgres@localhost:5432/miner_rename_file'
	db = SQLAlchemyEngine(db_url)
	db.create_all(True)
	repo = Repository('repo/terrame')
	sys = System('terrame', repo)
	session = db.create_session()
	session.add(repo)
	session.add(sys)
	session.commit()
	miner = RepositoryMiner(repo, sys)
	
	miner.extract(session, '082dff5e822ea1b4491911b7bf434a7f47a4be26')
	file = session.query(File).filter_by(fullpath = 'base/lua/Observer.lua').one()
	mod = session.query(Modification).filter_by(file_id = file.id).first()

	assert mod.new_path == 'base/lua/Observer.lua'
	assert mod.old_path == None
	assert mod.status == 'ADD'
	assert sys.file_exists('base/lua/Observer.lua')

	miner.extract(session, 'c57b6d69461abf10ba5950e0577dff3c982f3ea4')	
	file = session.query(File).filter_by(fullpath = 'src/lua/observer.lua').one()
	mod = session.query(Modification).filter_by(file_id = file.id).filter_by(status = 'RENAME').first()
	
	assert mod.new_path == 'src/lua/observer.lua'
	assert mod.old_path == 'base/lua/Observer.lua'
	assert mod.status == 'RENAME'
	assert sys.file_exists('src/lua/observer.lua')
	assert sys.file_exists('base/lua/Observer.lua')

	session.close()	
	db.drop_all()

def test_extract_same_commit():
	db_url = 'postgresql://postgres:postgres@localhost:5432/miner_rename_file'
	db = SQLAlchemyEngine(db_url)
	db.create_all(True)
	repo = Repository('repo/terrame')
	sys = System('terrame', repo)
	session = db.create_session()
	session.add(repo)
	session.add(sys)
	session.commit()
	miner = RepositoryMiner(repo, sys)
	
	miner.extract(session, '082dff5e822ea1b4491911b7bf434a7f47a4be26')
	file_count = session.query(File).count()	
	srcfile_count = session.query(SourceFile).count()
	mod_count = session.query(Modification).count()	

	#TODO(#41) miner.extract(session, '082dff5e822ea1b4491911b7bf434a7f47a4be26')

	assert file_count == session.query(File).count()
	assert srcfile_count == session.query(SourceFile).count()
	assert mod_count == session.query(Modification).count()

	session.close()	
	db.drop_all()
