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
								#print('@', from_fullpath, from_code_element.name, to_fullpath, to_code_element.name, '\n')
								from_info = RelationInfo()
								from_info.system = sys_from
								from_info.source_file = from_src_file
								from_info.code_element = from_code_element
								from_info.author = from_code_element.author()
								to_info = RelationInfo()
								to_info.system = sys_to
								to_info.source_file = to_src_file
								to_info.code_element = to_code_element
								to_info.author = to_code_element.author()
								rel = Relationship(from_info, to_info)
								#print(rel.__dict__)
								self.ecosystem.add_relationship(rel)

	#def _get_calls()