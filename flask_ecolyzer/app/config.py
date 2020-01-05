import os

class Config(object):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
		'postgresql://postgres:postgres@localhost:5432/ecosystem_last_commits'