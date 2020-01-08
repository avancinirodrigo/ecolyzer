from flask import jsonify, render_template, url_for
import json
from . import db
from . import bp as app
from ecolyzer.repository import Author, Modification
from ecolyzer.ecosystem import Relationship
from ecolyzer.system import Operation, SourceFile

@app.route('/authors')
def authors():
	authors = db.session.query(Author).all()
	return render_template('authors.html', authors=authors)

@app.route('/relationships', methods=['GET'])
def relationships():
	relations = db.session.query(Relationship).all()
	to_system = relations[0].to_system
	relations_count = []
	source_pos = {}
	paths = {}
	source_ids = []
	for rel in relations:
		source_id = rel.to_source_file_id
		if source_id in source_pos:
			pos = source_pos[source_id]
			relations_count[pos]['count'] = relations_count[pos]['count'] + 1
		else:
			source_pos[source_id] = len(relations_count)
			operations = db.session.query(Operation).\
						filter_by(source_file_id=source_id).count()						
			info = {
				'id': source_id,
				'source': rel.to_source_file.name(),
				'fullpath': rel.to_source_file.fullpath(),
				'path': rel.to_source_file.path(),
				'url': 'relationships/' + str(source_id),
				'system': rel.to_system.name,
				'operations': operations,
				'count': 1
			}
			relations_count.append(info)
			paths[rel.to_source_file.path()] = 0
			source_ids.append(source_id)

	sources_without_relation = db.session.query(SourceFile).\
					filter(SourceFile.id.notin_(source_ids)).\
					filter_by(system_id=to_system.id).all()
	sources_without_relation_info = []
	for src in sources_without_relation:
		operations = db.session.query(Operation).\
					filter_by(source_file_id=src.id).count()
		if operations > 0:		
			info = {
				'id': src.id,
				'source': src.name(),
				'fullpath': src.fullpath(),
				'path': src.path(),
				'url': '',
				'system': to_system.name,
				'operations': operations,
				'count': 0
			}
			sources_without_relation_info.append(info)
			paths[src.path()] = 0
	
	relations_count = relations_count + sources_without_relation_info

	return render_template('relations_count.html', relations=relations_count,
						system=to_system.name, paths=paths)

@app.route('/relationships/<int:id>', methods=['GET'])
def source_relations(id):
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
		else: # enter here just in the first time
			from_source_pos[from_source_id] = len(source_relations)
			from_systems[rel.from_system_id] = rel.from_system.name
			from_source_file = rel.from_source_file
			file_mod = db.session.query(Modification).\
						filter_by(file_id = from_source_file.file_id).one()	
			info = {
				'id': from_source_id,
				'from': from_source_file.name(),
				'fullpath': from_source_file.fullpath(),
				'code': rel.from_code_element.name + '()',
				'count': 1,
				'system': rel.from_system.name,
				'nloc': file_mod.nloc,
				'url': url_for('.source_codes', from_id=from_source_id, to_id=id)
			}
			source_relations.append(info)

	return render_template('source_relations.html', relations=source_relations,
						source_file=source_file.name(), from_systems=from_systems)

@app.route('/relationships/<int:from_id>/<int:to_id>', methods=['GET'])
def source_codes(from_id, to_id):
	relations = db.session.query(Relationship)\
					.filter_by(to_source_file_id = to_id,\
					from_source_file_id = from_id).all()
	from_file = relations[0].from_source_file.file
	to_file = relations[0].to_source_file.file
	from_system = relations[0].from_system.name
	to_system = relations[0].to_system.name
	from_source = db.session.query(Modification.source_code).\
					filter_by(file_id = from_file.id).one()
	to_source = db.session.query(Modification.source_code).\
					filter_by(file_id = to_file.id).one()					
	code_elements = []
	for rel in relations:
		# print(rel.to_code_element.name)
		code_elements.append(rel.to_code_element.name)
	return render_template('source_codes.html', from_source=from_source[0], 
						to_source=to_source[0], code_elements=code_elements,
						from_fullpath=from_file.fullpath, to_fullpath=to_file.fullpath,
						from_system=from_system, to_system=to_system)

@app.route('/blame', methods=['GET'])
def blame():
	return render_template('sources_blame.html')