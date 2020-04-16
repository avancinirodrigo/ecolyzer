from ecolyzer.system import System, Call, Operation
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
			for from_key, from_code_element in from_code_elements.items():
				if isinstance(from_code_element, Call):
					for to_fullpath, to_src_file in to_source_files.items():						
						to_operation = Operation(from_code_element.name, to_src_file)
						if to_src_file.code_element_exists(to_operation):	
							to_code_element = to_src_file.code_element_by_key(to_operation.key) 
							from_code_element_count = self._total_of_calls(from_code_element)
							from_info = FromRelationInfo(sys_from, from_src_file, 
											from_code_element, from_code_element_count)
							to_info = RelationInfo(sys_to, to_src_file, to_code_element)
							rel = Relationship(from_info, to_info)
							self.ecosystem.add_relationship(rel)
							session.add(rel)
						session.expunge(to_operation)
		session.commit()

	def _total_of_calls(self, from_code_element):
		analyzer = StaticAnalyzer()
		return analyzer.number_of_calls(from_code_element.source_code, from_code_element.name)
