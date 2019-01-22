from ecolyzer import GitAnalyzer

tags = [
	# None,
	# '1.4.0',
	# '1.5.0',
	# '1.6.0',
	# '2.0-BETA-1',
	# '2.0-BETA-2',
	# '2.0-BETA-3',
	# '2.0-BETA-4',
	# '2.0-BETA-5',
	# '2.0-RC-1',
	# '2.0-RC-2',
	# '2.0-RC-3',
	# '2.0-RC-4',
	'2.0-RC-5',
	'2.0-RC-6',
	'2.0-RC-7'
]

analyzer = GitAnalyzer('repo/terrame')
analyzer.set_tags(tags)
analyzer.extract_added_source_files()
analyzer.show_csv()