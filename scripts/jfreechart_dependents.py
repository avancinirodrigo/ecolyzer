import csv
from ecolyzer.repository import GitHub


repo_url = 'https://github.com/jfree/jfreechart'
gh = GitHub(repo_url)
dependents = gh.dependents()

list_all = []
list_forks = []
for dep in dependents:
	line = f'{dep.url},{dep.stars},{dep.forks}\n'
	list_all.append(line)
	if dep.forks > 2:
		list_forks.append(line)

file = open('jfreechart_dependents_all.csv', 'w')
file.writelines(list_all)
file.close()

file = open('jfreechart_dependents_forks.csv', 'w')
file.writelines(list_forks)
file.close()
