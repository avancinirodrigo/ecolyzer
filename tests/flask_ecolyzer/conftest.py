import pytest
from ecolyzer.dataaccess import SQLAlchemyORM
from ecolyzer.repository import Repository, RepositoryMiner
from ecolyzer.system import System
from ecolyzer.ecosystem import Ecosystem, EcosystemAnalyzer

@pytest.fixture(scope="module")
def db_connection():
    db_url = 'postgresql://postgres:postgres@localhost:5432/flask_test'
    db = SQLAlchemyORM(db_url)
    db.create_all(True)
    session = db.create_session()

    repo1 = Repository('repo/sci')
    sys1 = System('sci', repo1)

    session.add(repo1)
    session.add(sys1)

    miner = RepositoryMiner(repo1, sys1)
    miner.add_ignore_dir_with('tests')
    miner.add_ignore_dir_with('examples')    
    miner.extract_last_commits(session)

    repo2 = Repository('repo/sysdyn')
    sys2 = System('sysdyn', repo2)
    miner = RepositoryMiner(repo2, sys2)    
    miner.extract_last_commits(session)

    ecosystem = Ecosystem()

    ecolyzer = EcosystemAnalyzer(ecosystem)
    ecolyzer.make_relations(sys2, sys1, session)

    session.close()

    yield db_connection

    db.drop_all()