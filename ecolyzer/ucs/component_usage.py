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
		dependents_coverage = {}

		operations = self._get_operations(dataaccess)

		for rel in relations:
			operations[rel.to_code_element.name] += 1
			if (not self._operation) or (self._operation == rel.to_code_element.name):
				self._get_dependent(rel, source_relations,
									from_systems, from_source_pos, 
									dependents_coverage,
									dataaccess)			

		return {'component': {'name': source_file.name, 'operations': operations},
				'dependents': {'ids': from_systems, 'info': source_relations, 
				'coverage': dependents_coverage}}

	def _get_dependent(self, rel, source_relations, 
						from_systems, from_source_pos,
						dependents_coverage,
						dataaccess):
		from_source_id = rel.from_source_file_id
		if from_source_id in from_source_pos:
			pos = from_source_pos[from_source_id]
			source_relations[pos]['count'] += 1
			source_relations[pos]['ncalls'] += rel.from_code_element_count
		else: # enter here just in the first time
			from_source_pos[from_source_id] = len(source_relations)
			from_systems[rel.from_system_id] = rel.from_system.name
			from_source_file = rel.from_source_file
			file_mod = rel.from_code_element.modification
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

		self._add_dependent_coverage(rel.from_system.name, 
								rel.from_code_element.name,
								dependents_coverage)

	def _get_operations(self, dataaccess):
		operations_list = dataaccess.query(Operation).\
					filter_by(source_file_id = self._component_id).all()		
		operations = {}
		for op in operations_list:
			operations[op.name]	= 0
		return operations

	def _add_dependent_coverage(self, dependent_name, curr_call, 
								dependents_coverage):
		if dependent_name not in dependents_coverage:
			dependents_coverage[dependent_name] = {}
		if curr_call not in dependents_coverage[dependent_name]:
			dependents_coverage[dependent_name][curr_call] = 1
