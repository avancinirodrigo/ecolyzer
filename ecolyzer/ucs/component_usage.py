from ecolyzer.ecosystem import Relationship
from ecolyzer.repository import Modification
from ecolyzer.system import CodeElement, Operation


class ComponentUsage:
	"""ComponentUsage"""

	def __init__(self, component_id: int, operation: str = None):
		self._component_id = component_id
		self._operation = operation
				
	def execute(self, dataaccess, url_for):
		relations = dataaccess.query(Relationship).filter(
				Relationship.to_source_file_id == self._component_id).all()
		source_file = relations[0].to_source_file
		source_relations = []
		from_source_pos = {}
		from_systems = {}

		operations = self._get_operations(dataaccess)

		for rel in relations:
			operations[rel.to_code_element.name] += 1
			if (not self._operation) or (self._operation == rel.to_code_element.name):
				self._get_dependent(rel, source_relations,
									from_systems, from_source_pos, dataaccess, url_for)			

		return {'component': {'name': source_file.name, 'operations': operations},
				'dependents': {'ids': from_systems, 'info': source_relations}}

	def _get_dependent(self, rel, source_relations, 
						from_systems, from_source_pos,
						dataaccess, url_for):
		from_source_id = rel.from_source_file_id
		if from_source_id in from_source_pos:
			pos = from_source_pos[from_source_id]
			source_relations[pos]['count'] += 1
			source_relations[pos]['ncalls'] += rel.from_code_element_count
		else: # enter here just in the first time
			from_source_pos[from_source_id] = len(source_relations)
			from_systems[rel.from_system_id] = rel.from_system.name
			from_source_file = rel.from_source_file
			file_mod = dataaccess.query(Modification).\
						filter_by(file_id = from_source_file.file_id).one()	
			info = {
				'id': from_source_id,
				'from': from_source_file.name,
				'fullpath': from_source_file.fullpath,
				'count': 1,
				'system': rel.from_system.name,
				'nloc': file_mod.nloc,
				'ncalls': rel.from_code_element_count
			}
			source_relations.append(info)		

	def _get_operations(self, dataaccess):
		operations_list = dataaccess.query(Operation).\
					filter_by(source_file_id = self._component_id).all()		
		operations = {}
		for op in operations_list:
			operations[op.name]	= 0
		return operations
