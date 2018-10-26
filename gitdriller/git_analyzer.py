import pickle
from gitdriller.pydriller import PyDriller

class GitAnalyzer:

	def __init__(self, repo_path):
		self.repo_path = repo_path
		self.source_file_extensions = [
			'c', 'cc', 'cpp', 'h', 'hpp', 'hxx',
			'ui', 'qrc',
			'lua',
			'cmake', 'in',
			'photo',
			'sh',
			'bat',
			'rc',
			# 'log', # verificar
			'lp', 'css',
		]
		self.ignored_dirs = ['dependencies']
		self.source_files = {}

	def set_tags(self, tags):
		self.tags = tags

	def is_valid_dir(self, path):
		for ignored in self.ignored_dirs:
			if ignored in path:
				return False

		return True

	def extract_added_source_files(self):
		self.added_source_files = {}

		for i in range(1, len(self.tags)):
			self.added_source_files[self.tags[i]] = PyDriller().get_added_files_between_tags(
														self.repo_path,
														self.tags[i-1], self.tags[i]
													)
		self.set_source_files()

	def set_source_files(self):
		for tag in self.added_source_files:
			sources = []
			for i in range(0, len(self.added_source_files[tag])):
				source_file = self.added_source_files[tag][i]
				if (source_file.ext in self.source_file_extensions and
						self.is_valid_dir(source_file.path)):
					sources.append(self.added_source_files[tag][i])

			self.source_files[tag] = sources

	def csv_str(self, tag, file_number, source_file):
		return (tag + "," + str(file_number) + ","
					+ source_file.fullpath + ","
					+ source_file.ext + ","
					+ str(source_file.added))

	def show_csv(self):
		files_count = 0
		for tag in self.source_files:
			for i in range(0, len(self.source_files[tag])):
				source_file = self.source_files[tag][i]
				files_count += 1
				print(self.csv_str(tag, files_count, source_file))

	def save_csv(self, filename):
		file = open(filename, 'w')
		files_count = 0
		for tag in self.source_files:
			for i in range(0, len(self.source_files[tag])):
				source_file = self.source_files[tag][i]
				files_count += 1
				file.write(self.csv_str(tag, files_count, source_file) + '\n')
		file.close()

	def save(self, filename):
		file = open(filename, 'wb')
		pickle.dump(self.source_files, file)
		file.close()

	def load(self, filename):
		file = open(filename, 'rb')
		self.source_files = pickle.load(file)
		file.close()