from ecolyzer.system import System, Call, Operation, Association
from ecolyzer.dataaccess import NullSession
from ecolyzer.parser import StaticAnalyzer
from .relationship import Relationship, RelationInfo, FromRelationInfo

class EcosystemAnalyzer():
	"""EcosystemAnalyzer"""

	def __init__(self, ecosystem):
		self.ecosystem = ecosystem

	def make_relations(self, sys_from, sys_to, session=NullSession()):
		from_source_files = sys_from.source_files
		to_source_files = sys_to.source_files
		for from_fullpath, from_src_file in from_source_files.items():
			from_code_elements = from_src_file.code_elements()
			from_associations = self._get_associations(from_code_elements)			
			for to_fullpath, to_src_file in to_source_files.items():
				if (self._has_association(to_src_file, from_associations)
						or to_src_file.ext == 'lua'):
					for from_key, from_code_element in from_code_elements.items():
						if isinstance(from_code_element, Call):
							to_operation = Operation(from_code_element.name, to_src_file)
							if to_src_file.code_element_exists(to_operation):	
								to_code_element = to_src_file.code_element_by_key(to_operation.key) 
								from_code_element_count = self._total_of_calls(from_src_file,
															 from_code_element)
								from_info = FromRelationInfo(sys_from, from_src_file, 
												from_code_element, from_code_element_count)
								to_info = RelationInfo(sys_to, to_src_file, to_code_element)
								rel = Relationship(from_info, to_info)
								self.ecosystem.add_relationship(rel)
								session.add(rel)
							session.expunge(to_operation)
					session.commit()

	def _get_associations(self, code_elements):
		associations = []
		for element in code_elements.values():
			if isinstance(element, Association):		
				associations.append(element.name)
		return associations

	def _has_association(self, source_file, associations):
		for assoc in associations:
			if assoc in source_file.fullpath:
				return True
		return False

	def _total_of_calls(self, from_source_file, from_code_element):
		analyzer = StaticAnalyzer()
		return analyzer.number_of_calls(from_source_file, from_code_element.source_code, from_code_element.name)
