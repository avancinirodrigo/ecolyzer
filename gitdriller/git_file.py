import os

class GitFile:
	def __init__(self, fullpath):
		path, ext = os.path.splitext(fullpath)
		ext = ext.split(".")[-1]
		self.fullpath = fullpath
		self.path = path
		# self.name = name
		self.ext = ext
		self.added = 0