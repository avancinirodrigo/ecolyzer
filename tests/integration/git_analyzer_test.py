import unittest
import time
import filecmp
import os
from gitdriller import GitAnalyzer

class GitAnalyzerTest(unittest.TestCase):

	def test_save(self):
		tags = [
			'2.0-RC-5',
			'2.0-RC-6',
			'2.0-RC-7'
		]

		analyzer = GitAnalyzer('D:/win/terrame/git/terrame')
		analyzer.set_tags(tags)
		analyzer.extract_added_source_files()
		#analyzer.show_csv()
		filename = 'save' + str(int(time.time())) + '.pkl'
		#filepath = os.path.join(os.path.dirname(__file__), filename)
		filetest = os.path.join(os.path.dirname(__file__), 'data', 'save_test1.pkl')
		analyzer.save(filename)
		self.assertTrue(filecmp.cmp(filetest, filename))
		os.remove(filename)
		#print(os.path.join(os.path.dirname(__file__), 'data', 'save_test1.pkl'))

if __name__ == '__main__':
	unittest.main()