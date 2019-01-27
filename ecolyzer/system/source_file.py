import os

class SourceFile():
	def __init__(self, fullpath):
		path, file_ext = os.path.split(fullpath)
		file, ext = file_ext.split('.')
		self.fullpath = fullpath
		self.path = path
		self.name = file
		self.ext = ext
