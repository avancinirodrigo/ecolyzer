from ecolyzer.repository import RepositoryMiner, Repository, CommitInfo, Commit, Author
from ecolyzer.system import System
from ecolyzer.dataaccess import SQLAlchemyEngine

db_url = 'postgresql://postgres:postgres@localhost:5432/miner_test'
db = SQLAlchemyEngine(db_url)
db.create_all(True)

def test_get_commit():
	repo = Repository('repo/terrame')
	sys = System('terrame', repo)
	miner = RepositoryMiner(repo.path)
	commit_info = miner.get_commit_info('80a562be869dbb984229f608ae9a04d05c5e1689')

	assert commit_info.msg == 'Initial commit'
	assert commit_info.date.strftime('%Y-%m-%d %H:%M:%S') == '2014-09-15 08:12:11'
	assert commit_info.hash == '80a562be869dbb984229f608ae9a04d05c5e1689'
	assert commit_info.author_name == 'pedro-andrade-inpe'
	assert commit_info.author_email == 'pedro.andrade@inpe.br'

	author = Author(commit_info.author_name, commit_info.author_email)
	commit = Commit(commit_info, author, repo)
	
	session = db.create_session()
	session.add(repo)
	session.add(sys)
	session.add(commit)
	session.commit()

	commitdb = session.query(Commit).get(1)

	assert commitdb.msg == 'Initial commit'
	assert commitdb.date.strftime('%Y-%m-%d %H:%M:%S') == '2014-09-15 08:12:11'
	assert commitdb.hash == '80a562be869dbb984229f608ae9a04d05c5e1689'
	assert commitdb.repository.path == repo.path
	assert commitdb.author.name == 'pedro-andrade-inpe'
	assert commitdb.author.email == 'pedro.andrade@inpe.br'	

	commit_info = miner.get_commit_info('ffb8347b2de44eb05f6c5eba3b3cb8b7716acebb')

	assert commit_info.msg == 'Delete LICENSE'
	assert commit_info.date.strftime('%Y-%m-%d %H:%M:%S') == '2014-09-17 11:49:45'
	assert commit_info.hash == 'ffb8347b2de44eb05f6c5eba3b3cb8b7716acebb'
	assert commit_info.author_name == 'pedro-andrade-inpe'
	assert commit_info.author_email == 'pedro.andrade@inpe.br'

	commit = Commit(commit_info, author, repo)
	session.add(commit)
	session.commit()

	commitdb2 = session.query(Commit).get(2)

	assert commitdb2.msg == 'Delete LICENSE'
	assert commitdb2.date.strftime('%Y-%m-%d %H:%M:%S') == '2014-09-17 11:49:45'
	assert commitdb2.hash == 'ffb8347b2de44eb05f6c5eba3b3cb8b7716acebb'
	assert commitdb2.repository.id == repo.id
	assert commitdb2.author.name == 'pedro-andrade-inpe'
	assert commitdb2.author.email == 'pedro.andrade@inpe.br'		

	commitdb1 = session.query(Commit).get(1)

	assert commitdb1.msg == 'Initial commit'
	assert commitdb1.date.strftime('%Y-%m-%d %H:%M:%S') == '2014-09-15 08:12:11'
	assert commitdb1.hash == '80a562be869dbb984229f608ae9a04d05c5e1689'
	assert commitdb1.repository.path == repo.path	
	assert commitdb2.author.name == 'pedro-andrade-inpe'
	assert commitdb2.author.email == 'pedro.andrade@inpe.br'	

	session.close()
	db.drop_all()
