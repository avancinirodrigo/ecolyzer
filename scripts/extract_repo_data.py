from ecolyzer.repository import RepositoryMiner, Repository
from ecolyzer.system import System
from ecolyzer.dataaccess import SQLAlchemyEngine

db_url = 'postgresql://postgres:postgres@localhost:5432/extract_repo_data'
db = SQLAlchemyEngine(db_url)
db.create_all(True)
session = db.create_session()

repo1 = Repository('repo/terrame')
sys1 = System('terrame', repo1)
miner = RepositoryMiner(repo1, sys1)
miner.extract(session)

repo2 = Repository('repo/ca')
sys2 = System('ca', repo2)
miner = RepositoryMiner(repo2, sys2)
miner.extract(session)

session.close()
