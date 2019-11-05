from flask import jsonify, render_template, url_for
import json
from app import app, db
from ecolyzer.repository import Author #Repository, Author, Person.
#from ecolyzer.ecosystem import Ecosystem
from ecolyzer.ecosystem import Relationship

@app.route('/authors')
def authors():
	authors = db.session.query(Author).all()
	#resp = ''
	#for a in authors:
	#	resp += '<p>' + a.person.name + ': ' + a.person.email + '</p>'

	#return resp
	return render_template('authors.html', authors=authors)

@app.route('/relationships', methods=['GET'])
def relationships():
	relations = db.session.query(Relationship).all()
	to_system = relations[0].to_system.name
	file_relations = {}
	for rel in relations:
		to_code_element = rel.to_code_element
		#key = to_code_element.source_file.fullpath()
		key = to_code_element.source_file.id 
		if key not in file_relations:
			file_relations[key] = {}
			file_relations[key]['id'] = rel.id
			file_relations[key]['source'] = to_code_element.source_file.name()	
			file_relations[key]['path'] = to_code_element.source_file.path()	
			file_relations[key]['count'] = 0		
			file_relations[key]['url'] = url_for('relationships', id=key)		
		#rel_dict = row_to_dict(rel)
		#rel_dict = {}
		#rel_dict.source = str(to_code_element.source_file.name())
		#rel_dict.id = rel.id
		
		#file_relations[to_code_element.source_file.fullpath()].append(rel_dict)
		file_relations[key]['count'] = file_relations[key]['count'] + 1
		#file_relations[to_code_element.source_file.fullpath()].append(rel)

	#return json.dumps(file_relations)
	return render_template('relationships.html', relations=file_relations,
						system=to_system)
	#return jsonify(relations=file_relations)

@app.route('/relationships/<int:id>', methods=['GET'])
def get_relationship(id):
	relations = db.session.query(Relationship).filter_by(to_source_file_id = id).all()
	source_file = relations[0].to_source_file #db.session.query(SourceFile).get(id)
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
						source_file=source_file.name(), from_systems=from_systems) #jsonify(row_to_dict(rel))

def row_to_dict(row):
	d = {}
	for column in row.__table__.columns:
		d[column.name] = str(getattr(row, column.name))
	return d
