from flask import render_template, url_for, request
from . import db
from . import bp as app
from ecolyzer.ucs import (CentralSoftwareUsage, ComponentUsage,
						ComponentsSideBySide, ComponentSourceCode)


@app.route('/', methods=['GET'])
@app.route('/relationships', methods=['GET'])
def relationships():
	dataaccess = db.session
	uc = CentralSoftwareUsage()
	central_software_info = uc.execute(dataaccess)
	components = central_software_info['components']
	for comp in components:
		if comp['count'] > 0:
			comp['url'] = url_for('.component_usage', id=comp['id'])
		else:
			comp['url'] = url_for('.component_source_code', id=comp['id'])
	dataaccess.close()
	return render_template('central_software_usage.html', 
						relations=central_software_info['components'],
						system=central_software_info['central_software'], 
						paths=central_software_info['component_paths'],
						dependents_count=central_software_info['dependents_count'],
						dependents_by_package=central_software_info['dependents_by_package'])


@app.route('/relationships/<int:id>', methods=['GET'])
def component_usage(id):
	operation = request.args.get('operation', default=None, type=str)
	dataaccess = db.session
	uc = ComponentUsage(id, operation)
	component_info = uc.execute(dataaccess, url_for)
	dependents = component_info['dependents']['info']
	for dep in dependents:
		dep['url'] = url_for('.source_codes', from_id=dep['id'], to_id=id)
	component_url = url_for('.component_usage', id=id)
	return render_template('component_usage.html', 
						relations=component_info['dependents']['info'],
						source_file=component_info['component']['name'], 
						from_systems=component_info['dependents']['ids'],
						operations=component_info['component']['operations'],
						dependents_coverage=component_info['dependents']['coverage'],
						component_url=component_url,
						selected_operation=operation)


@app.route('/relationships/<int:from_id>/<int:to_id>', methods=['GET'])
def source_codes(from_id, to_id):
	dataaccess = db.session
	uc = ComponentsSideBySide(to_id, from_id)
	components_info = uc.execute(dataaccess)
	central = components_info['central']
	dependent = components_info['dependent']
	return render_template('components_side_by_side.html', from_source=dependent['source_code'], 
						to_source=central['source_code'], code_elements=central['code_elements'],
						dependent_refs=dependent['code_elements'],
						from_fullpath=dependent['fullpath'], to_fullpath=central['fullpath'],
						from_system=dependent['system'], to_system=central['system'], 
						language=components_info['language'])


@app.route('/source_code/<int:id>', methods=['GET'])	
def component_source_code(id):
	dataaccess = db.session
	uc = ComponentSourceCode(id)
	component_info = uc.execute(dataaccess)
	return render_template('component_source_code.html', 
						source_code=component_info['source_code'],
						name=component_info['name'], 
						fullpath=component_info['fullpath'], 
						system_name=component_info['system'], 
						language=component_info['language'])	
