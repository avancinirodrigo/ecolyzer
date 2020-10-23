from flask import jsonify, render_template, url_for
import json
from . import db
from . import bp as app
from ecolyzer.repository import Author, Modification
from ecolyzer.ecosystem import Relationship
from ecolyzer.system import Operation, SourceFile
from ecolyzer.ucs import CentralSoftwareUsage

@app.route('/', methods=['GET'])
@app.route('/relationships', methods=['GET'])
def relationships():
	dataaccess = db.session
	uc = CentralSoftwareUsage()
	central_software_info = uc.execute(dataaccess)
	components = central_software_info['components']
	for comp in components:
		if comp['operations'] > 0:
			comp['url'] = url_for('.source_relations', id=comp['id'])
	dataaccess.close()
	return render_template('relations_count.html', 
						relations=central_software_info['components'],
						system=central_software_info['central_software'].name, 
						paths=central_software_info['component_paths'])

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
			source_relations[pos]['count'] += 1
			source_relations[pos]['ncalls'] += rel.from_code_element_count
		else: # enter here just in the first time
			from_source_pos[from_source_id] = len(source_relations)
			from_systems[rel.from_system_id] = rel.from_system.name
			from_source_file = rel.from_source_file
			file_mod = db.session.query(Modification).\
						filter_by(file_id = from_source_file.file_id).one()	
			info = {
				'id': from_source_id,
				'from': from_source_file.name,
				'fullpath': from_source_file.fullpath,
				'code': rel.from_code_element.name + '()',
				'count': 1,
				'system': rel.from_system.name,
				'nloc': file_mod.nloc,
				'ncalls': rel.from_code_element_count,
				'url': url_for('.source_codes', from_id=from_source_id, to_id=id)
			}
			source_relations.append(info)

	return render_template('source_relations.html', relations=source_relations,
						source_file=source_file.name, from_systems=from_systems)

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

	language = ''
	if to_file.ext == 'lua':
		language = 'lua'
	elif to_file.ext == 'java':
		language = 'java'

	return render_template('source_codes.html', from_source=from_source[0], 
						to_source=to_source[0], code_elements=code_elements,
						from_fullpath=from_file.fullpath, to_fullpath=to_file.fullpath,
						from_system=from_system, to_system=to_system, language=language)
