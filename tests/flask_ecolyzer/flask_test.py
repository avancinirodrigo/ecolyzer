import pytest
import os
#from flask import json
from flask import template_rendered
from contextlib import contextmanager
from flask_ecolyzer.app import create_app
from flask_ecolyzer.app.config import Config

class TestConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/flask_test'

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

def test_relationships(app, client, db_connection):
	with get_context_variables(app) as contexts:
		res = client.get('/relationships')
		contexts = next(contexts)
		system = contexts['system']
		relations = contexts['relations']
		paths = contexts['paths']
		assert system == 'TerraME'
		assert len(relations) == 53
		assert len(paths) == 9

def get_source_id(relations, name):
	for rel in relations:
		if rel['source'] == name:
			return rel['id']	

def test_source_relations(app, client, db_connection):
	source_id = None
	with get_context_variables(app) as contexts:
		res = client.get('/relationships')
		contexts = next(contexts)
		relations = contexts['relations']
		source_id = get_source_id(relations, 'CellularSpace')

	with get_context_variables(app) as contexts:
		res = client.get('/relationships/' + str(source_id))
		contexts = next(contexts)
		print(contexts)