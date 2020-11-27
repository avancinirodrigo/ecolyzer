from ecolyzer.repository import Modification
from ecolyzer.system import SourceFile


class ComponentSourceCode():
	"""ComponentSourceCode"""

	def __init__(self, source_id):
		self._source_id = source_id
		
	def execute(self, dataaccess):
		source_file = dataaccess.query(SourceFile).\
					filter_by(id=self._source_id).one()
		source_code = dataaccess.query(Modification.source_code).\
						filter_by(file_id = self._source_id).one()					
		system = source_file.system.name
		language = ''
		if source_file.ext == 'lua':
			language = 'lua'
		elif source_file.ext == 'java':
			language = 'java'	

		return {'source_code': source_code[0], 
				'name': source_file.name,
				'fullpath': source_file.fullpath, 
				'system': system,
				'language': language}
