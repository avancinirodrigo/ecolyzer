from flask import jsonify, render_template, url_for, request
import json
from . import db
from . import bp as app
from ecolyzer.repository import Author, Modification
from ecolyzer.ecosystem import Relationship
from ecolyzer.system import Operation, SourceFile
from ecolyzer.ucs import CentralSoftwareUsage, ComponentUsage


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
	operation = request.args.get('operation', default = None, type = str)
	dataaccess = db.session
	uc = ComponentUsage(id, operation)
	component_info = uc.execute(dataaccess, url_for)
	dependents = component_info['dependents']['info']
	for dep in dependents:
		dep['url'] = url_for('.source_codes', from_id = dep['id'], to_id = id)
	component_url = url_for('.source_relations', id = id)
	return render_template('source_relations.html', 
						relations=component_info['dependents']['info'],
						source_file=component_info['component']['name'], 
						from_systems=component_info['dependents']['ids'],
						operations=component_info['component']['operations'],
						component_url=component_url,
						selected_operation=operation)

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
