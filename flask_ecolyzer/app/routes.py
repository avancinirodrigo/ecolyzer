from flask import jsonify, render_template
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
	#ecos = Ecosystem()
	relations = db.session.query(Relationship).all() #ecos.relationships()
	file_relations = {}
	for rel in relations:
		to_code_element = rel.to_code_element
		#to_source_file = to_code_element.fullpath()
		#to_system = rel.to_system.name
		#from_code_element = rel.from_code_element
		#print(to_code_element.name, to_code_element.source_file.fullpath())
		if to_code_element.source_file.fullpath() not in file_relations:
			file_relations[to_code_element.source_file.fullpath()] = []			
		file_relations[to_code_element.source_file.fullpath()].append(row_to_dict(rel))
	
	#return json.dumps(file_relations)
	#return render_template('relations.html', relations=file_relations)
	return jsonify(file_relations)

@app.route('/relationships/<int:id>', methods=['GET'])
def get_relationship(id):
	rel = db.session.query(Relationship).get(id)
	print(row_to_dict(rel))
	return jsonify(row_to_dict(rel))

def row_to_dict(row):
	d = {}
	for column in row.__table__.columns:
		d[column.name] = str(getattr(row, column.name))
	return d
