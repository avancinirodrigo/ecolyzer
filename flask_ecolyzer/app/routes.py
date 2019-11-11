from flask import jsonify, render_template, url_for
import json
from app import app, db
from ecolyzer.repository import Author
from ecolyzer.ecosystem import Relationship

@app.route('/authors')
def authors():
	authors = db.session.query(Author).all()
	return render_template('authors.html', authors=authors)

@app.route('/relationships', methods=['GET'])
def relationships():
	relations = db.session.query(Relationship).all()
	to_system = relations[0].to_system.name
	relations_count = []
	source_pos = {}
	for rel in relations:
		source_id = rel.to_source_file_id
		if source_id in source_pos:
			pos = source_pos[source_id]
			relations_count[pos]['count'] = relations_count[pos]['count'] + 1
		else:
			source_pos[source_id] = len(relations_count)
			info = {
				'id': rel.to_source_file_id,
				'source': rel.to_source_file.name(),
				'url': url_for('relationships', id=source_id),
				'system': rel.to_system.name,
				'count': 1
			}
			relations_count.append(info)

	return render_template('relations_count.html', relations=relations_count,
						system=to_system)

@app.route('/relationships/<int:id>', methods=['GET'])
def get_relationship(id):
	relations = db.session.query(Relationship).filter_by(to_source_file_id = id).all()
	source_file = relations[0].to_source_file
	source_relations = []
	from_source_pos = {}
	from_systems = {}
	for rel in relations:
		from_source_id = rel.from_source_file_id
		if from_source_id in from_source_pos:
			pos = from_source_pos[from_source_id]
			source_relations[pos]['count'] = source_relations[pos]['count'] + 1
		else:
			from_source_pos[from_source_id] = len(source_relations)
			from_systems[rel.from_system_id] = rel.from_system.name
			info = {
				'id': rel.from_source_file_id,
				'from': rel.from_source_file.name(),
				'code': rel.from_code_element.name + '()',
				'count': 1,
				'system': rel.from_system.name
			}
			source_relations.append(info)

	return render_template('source_relations.html', relations=source_relations,
						source_file=source_file.name(), from_systems=from_systems)

@app.route('/blame', methods=['GET'])
def blame():
	return render_template('sources_blame.html')