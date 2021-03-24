import os


class Config(object):
	SERVER_URL = os.environ.get('SERVER_URL') or 'http://127.0.0.1:5000'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
	'postgresql://postgres:postgres@localhost:5432/ecosystem_last_commits'
