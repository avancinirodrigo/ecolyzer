import time
import filecmp
import os
from ecolyzer import GitAnalyzer

tags = [
	'2.0-RC-5',
	'2.0-RC-6',
	'2.0-RC-7'
]

analyzer = GitAnalyzer('repo/terrame')
analyzer.set_tags(tags)
analyzer.extract_added_source_files()

def test_save_csv():
	filename = 'save' + str(int(time.time()))
	file_csv = filename + '.csv'
	analyzer.save_csv(file_csv)
	filetest_csv = os.path.join(os.path.dirname(__file__), 'data', 'save_test1.csv')
	assert filecmp.cmp(filetest_csv, file_csv)
	os.remove(file_csv)

def test_save_pkl():
	filename = 'save' + str(int(time.time()))
	file_pkl = filename + '.pkl'
	analyzer.save(file_pkl)

	analyzer_pkl = GitAnalyzer('repo/terrame')
	analyzer_pkl.load(file_pkl)
	file_csv = filename + '.csv'
	analyzer_pkl.save_csv(file_csv)

	filetest_pkl = os.path.join(os.path.dirname(__file__), 'data', 'save_test1.pkl')
	filetest_csv = filename + 'test.csv'
	analyzer_pkl.save_csv(filetest_csv)

	assert filecmp.cmp(filetest_csv, file_csv)
	os.remove(file_pkl)
	os.remove(file_csv)
	os.remove(filetest_csv)

def test_save_db():
	tags = [
		'2.0-RC-5',
		'2.0-RC-6',
		'2.0-RC-7'
	]

	analyzer = GitAnalyzer('repo/terrame')
	analyzer.set_tags(tags)
	analyzer.extract_added_source_files_todb(True)
	sources = analyzer.load_db(analyzer.repo_name)
	file_csv = 'save_db.csv'
	analyzer.save_csv(file_csv)
	filetest_csv = os.path.join(os.path.dirname(__file__), 'data', 'save_test1.csv')
	assert filecmp.cmp(filetest_csv, file_csv)
	os.remove(file_csv)
