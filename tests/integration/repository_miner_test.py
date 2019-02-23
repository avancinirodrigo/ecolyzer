from ecolyzer.repository import RepositoryMiner, Repository, CommitInfo, Commit, Author, Modification
from ecolyzer.system import System, File
from ecolyzer.dataaccess import SQLAlchemyEngine

db_url = 'postgresql://postgres:postgres@localhost:5432/miner_test'
	
def test_get_commit():
	db = SQLAlchemyEngine(db_url)
	db.create_all(True)
	repo = Repository('repo/terrame')
	sys = System('terrame', repo)
	miner = RepositoryMiner(repo)
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
	assert commit_info.modifications[0].type == 'ADD'

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
	assert filemoddb.type == 'ADD'

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
	assert commit_info.modifications[0].type == 'DELETE'

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
	assert filemoddb2.type == 'DELETE'	

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
	assert filemoddb1.type == 'ADD'	

	session.close()
	db.drop_all()
	
def test_extract():
	db = SQLAlchemyEngine(db_url)
	db.create_all(True)
	repo = Repository('repo/terrame')
	sys = System('terrame', repo)
	session = db.create_session()
	session.add(repo)
	session.add(sys)
	session.commit()
	miner = RepositoryMiner(repo)
	miner.extract(session, '082dff5e822ea1b4491911b7bf434a7f47a4be26')
	session.close()
	db.drop_all()
