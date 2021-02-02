from ecolyzer.dataaccess import SQLAlchemyORM
from ecolyzer.ucs import MappingEcosystemDependents


db_url = 'postgresql://postgres:postgres@localhost:5432/jfreechart_ecosystem'
db = SQLAlchemyORM(db_url)
db.create_all(True)

repo_url = 'https://github.com/jfree/jfreechart'
uc = MappingEcosystemDependents(repo_url, 
								branch='master', 
								ecosystem_name='JFreeChart',
								forks=100,
								ignore_dirs_with=['test'])

dataaccess = db.create_session()
uc.execute(dataaccess)

dataaccess.commit()
dataaccess.close()
