from ecolyzer.ecosystem import Relationship
from ecolyzer.repository import Modification
from ecolyzer.parser import StaticAnalyzer
from ecolyzer.system import Call


class ComponentsSideBySide():
	"""ComponentsSideBySide"""

	def __init__(self, central_source_id, dependent_source_id):
		self._central_source_id = central_source_id
		self._dependent_source_id = dependent_source_id
		
	def execute(self, dataaccess):
		from_id = self._dependent_source_id
		to_id = self._central_source_id 
		relations = dataaccess.query(Relationship)\
						.filter_by(to_source_file_id = to_id,\
						from_source_file_id = from_id).all()
		from_file = relations[0].from_source_file.file
		to_file = relations[0].to_source_file.file
		from_system = relations[0].from_system.name
		to_system = relations[0].to_system.name
		from_source = relations[0].from_code_element.modification.source_code 
		to_source = relations[0].to_code_element.modification.source_code 
				
		code_elements = []
		code_elements_map = {}
		for rel in relations:
			name = rel.to_code_element.name.split('.')
			print('   ', rel.to_code_element.name, rel.from_code_element_count)
			if len(name) > 1:
				name = name[1]
			else:
				name = name[0]
			code_elements.append(name)
			code_elements_map[rel.to_code_element.name] = name

		language = ''
		if to_file.ext == 'lua':
			language = 'lua'
		elif to_file.ext == 'java':
			language = 'java'	

		references = self._references(from_file, from_source, code_elements_map)
		#references = self._references(from_id, code_elements_map, dataaccess)

		central = {'source_code': to_source, 
					'fullpath': to_file.fullpath, 
					'system': to_system,
					'code_elements': code_elements}			
		dependent = {'source_code': from_source, 
					'fullpath': from_file.fullpath, 
					'system': from_system,
					'code_elements': references}

		for ref in references:
			print('    ', ref)

		return {'central': central,
				'dependent': dependent,
				'language': language}

	def _references(self, source_file, source_code, code_elements_map):
		analyzer = StaticAnalyzer()
		refs = analyzer.references(source_file, source_code)	
		references = []	
		for ref in refs:
			if ref['ref'] in code_elements_map:
				name = code_elements_map[ref['ref']]
				references.append(self._get_reference(ref['caller'], name))
		return references

	# TODO: remove after some acceptance tests
	# def _references(self, dependent_source_id, code_elements_map, dataaccess):
	# 	refs = dataaccess.query(Call).\
	# 			filter_by(source_file_id = dependent_source_id).all()
	# 	references = []	
	# 	for ref in refs:
	# 		if ref.name in code_elements_map:
	# 			name = code_elements_map[ref.name]
	# 			references.append(self._get_reference(ref.caller, name))
	# 	return references		

	def _get_reference(self, caller, name):
		if caller:
			if caller == 'extends': # TODO: standarlize reference for aways two fields class.ref
				return f'{name}.{caller}' 
			return f'{caller}.{name}' 	
		return f'{name}'			