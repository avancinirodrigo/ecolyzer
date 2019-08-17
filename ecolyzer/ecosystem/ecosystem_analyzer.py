from ecolyzer.system import System, Call, Operation
from .relationship import Relationship, RelationInfo

class EcosystemAnalyzer():
	"""EcosystemAnalyzer"""

	def __init__(self, ecosystem):
		self.ecosystem = ecosystem

	def make_relations(self, sys_to, sys_from, session=None):
		from_source_files = sys_from.source_files
		to_source_files = sys_to.source_files
		for from_fullpath, from_src_file in from_source_files.items(): 
			from_code_elements = from_src_file.code_elements()
			for from_name, from_code_element in from_code_elements.items():
				if isinstance(from_code_element, Call):
					for to_fullpath, to_src_file in to_source_files.items():
						if to_src_file.code_element_exists(from_name):	
							to_code_element = to_src_file.code_element_by_name(from_name) 
							if to_code_element and isinstance(to_code_element, Operation):
								from_info = RelationInfo(sys_from, from_src_file, from_code_element)
								to_info = RelationInfo(sys_to, to_src_file, to_code_element)
								rel = Relationship(from_info, to_info)
								self.ecosystem.add_relationship(rel)
								