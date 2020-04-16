import pytest
import os
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

def get_url_by_key(relations, name, key):
	for rel in relations:
		if rel[key] == name:
			return rel['url']

def get_source_url(relations, name):
	return get_url_by_key(relations, name, 'source')

def get_from_url(relations, name):
	return get_url_by_key(relations, name, 'from')					

def test_source_relations(app, client, db_connection):
	source_relations_url = None
	with get_context_variables(app) as contexts:
		res = client.get('/relationships')
		contexts = next(contexts)
		relations = contexts['relations']
		from_system_id = relations
		source_relations_url = get_source_url(relations, 'CellularSpace')

	with get_context_variables(app) as contexts:
		res = client.get(source_relations_url)
		contexts = next(contexts)
		from_systems = contexts['from_systems']
		relations = contexts['relations']
		source_name = contexts['source_file']
		assert len(from_systems) == 1
		assert 'CA' in from_systems.values()
		assert len(relations) == 32
		assert source_name == 'CellularSpace'

def test_source_codes(app, client, db_connection):
	source_relations_url = None
	with get_context_variables(app) as contexts:
		res = client.get('/relationships')
		contexts = next(contexts)
		relations = contexts['relations']
		from_system_id = relations
		source_relations_url = get_source_url(relations, 'CellularSpace')

	source_codes_url = None
	with get_context_variables(app) as contexts:
		res = client.get(source_relations_url)
		contexts = next(contexts)
		relations = contexts['relations']
		source_codes_url = get_from_url(relations, 'Influenza')		

	with get_context_variables(app) as contexts:
		res = client.get(source_codes_url)
		contexts = next(contexts)
		code_elements = contexts['code_elements']
		assert len(code_elements) == 4
