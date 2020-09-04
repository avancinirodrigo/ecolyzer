import os
import shutil


class FileUtils():

	@staticmethod
	def split(fullpath):
		path, file_with_ext = os.path.split(fullpath)
		filename = ''
		ext = ''
		if '.' in file_with_ext:
			split_list = file_with_ext.split('.')
			if len(split_list) > 2:
				ext = split_list.pop()
				filename = '.'.join(split_list)
			else:
				if file_with_ext.startswith('.'):
					filename = '.' + split_list[1]
				else:
					filename = split_list[0]
					ext = split_list[1]
		else:
			filename = file_with_ext		

		return path, filename, ext

	@staticmethod
	def last_dir(path: str) -> str:
		return os.path.basename(os.path.normpath(path))

	@staticmethod
	def rmdir(path: str):
		shutil.rmtree(path, ignore_errors=True)

	@staticmethod
	def extension(fullpath):
		path, file_with_ext = os.path.split(fullpath)
		ext = ''
		if '.' in file_with_ext:
			split_list = file_with_ext.split('.')
			if len(split_list) > 2:
				ext = split_list.pop()
			else:
				if not file_with_ext.startswith('.'):
					ext = split_list[1]
		return ext		
