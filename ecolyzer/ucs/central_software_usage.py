from ecolyzer.ecosystem import Relationship
from ecolyzer.system import Operation, SourceFile
from ecolyzer.repository import Modification


class CentralSoftwareUsage:
	"""CentralSoftwareUsage"""
		
	def execute(self, dataaccess):
		relations = dataaccess.query(Relationship).all()
		to_system = relations[0].to_system
		components = []
		source_pos = {}
		paths = {}
		source_ids = []
		component_operations = {}
		for rel in relations:
			source_id = rel.to_source_file_id
			curr_operation = rel.to_code_element.name
			if source_id in source_pos:
				pos = source_pos[source_id]
				components[pos]['count'] += 1
				if component_operations[source_id][curr_operation]:
					component_operations[source_id][curr_operation] = False
					components[pos]['coverage'] += 1
			else:
				source_pos[source_id] = len(components)
				operations = dataaccess.query(Operation).\
							filter_by(source_file_id=source_id).all()
				component_operations[source_id] = {}
				for op in operations:
					component_operations[source_id][op.name] = True
				component_operations[source_id][curr_operation] = False 

				file_mod = dataaccess.query(Modification).\
							filter_by(file_id = rel.to_source_file.file_id).one()					
				info = {
					'id': source_id,
					'source': rel.to_source_file.name,
					'fullpath': rel.to_source_file.fullpath,
					'path': rel.to_source_file.path,
					'system': rel.to_system.name,
					'operations': len(operations),
					'nloc': file_mod.nloc,
					'coverage': 1,
					'count': 1
				}
				components.append(info)
				paths[rel.to_source_file.path] = 0
				source_ids.append(source_id)

		sources_without_relation = dataaccess.query(SourceFile).\
						filter(SourceFile.id.notin_(source_ids)).\
						filter_by(system_id=to_system.id).all()
		sources_without_relation_info = []
		for src in sources_without_relation:
			operations = dataaccess.query(Operation).\
						filter_by(source_file_id=src.id).count()
			if operations > 0:		
				file_mod = dataaccess.query(Modification).\
							filter_by(file_id = src.file_id).one()
				info = {
					'id': src.id,
					'source': src.name,
					'fullpath': src.fullpath,
					'path': src.path,
					'system': to_system.name,
					'operations': operations,
					'nloc': file_mod.nloc,
					'coverage': 0,
					'count': 0
				}
				sources_without_relation_info.append(info)
				paths[src.path] = 0
		
		components = components + sources_without_relation_info	

		return {'components': components, 'central_software': to_system,
				'component_paths': paths}
