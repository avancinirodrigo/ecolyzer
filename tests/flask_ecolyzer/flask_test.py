import pytest
import os
#from flask import json
from flask import template_rendered
from contextlib import contextmanager
from flask_ecolyzer.app import create_app
from flask_ecolyzer.app.config import Config

class TestConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
			'postgresql://postgres:postgres@localhost:5432/ecosystem_last_commits'

#https://stackoverflow.com/questions/39822265/flask-testing-how-to-retrieve-variables-that-were-passed-to-jinja
@contextmanager
def get_context_variables(app):
    recorded = []
    def record(sender, template, context, **extra):
        recorded.append(context)
    template_rendered.connect(record, app)
    try:
        yield iter(recorded)
    finally:
        template_rendered.disconnect(record, app)

@pytest.fixture
def app():
    app = create_app(TestConfig)
    return app

def test_relationships(app, client):
	with get_context_variables(app) as contexts:
		res = client.get('/relationships')
		contexts = next(contexts)
		assert contexts['system'] == 'terrame'