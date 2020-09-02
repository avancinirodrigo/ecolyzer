from ecolyzer.repository import GitHub


def test_dependents():
	repo_url = 'https://github.com/apache/hadoop'
	gh = GitHub(repo_url)
	dependents = gh.dependents()
	assert len(dependents) >= 56
	for dep in dependents:
		assert dep.stars >= 0
		assert dep.url is not None
		assert dep.url != repo_url
		assert dep.forks >= 0


def test_dependents_stars():
	repo_url = 'https://github.com/apache/hadoop'
	gh = GitHub(repo_url)	
	dependents = gh.dependents(5)
	assert len(dependents) >= 5
	for dep in dependents:
		assert dep.stars >= 5
		assert dep.url is not None
		assert dep.url != repo_url
		assert dep.forks >= 0

def test_dependents_withou_next_url():
	repo_url = 'https://github.com/scribejava/scribejava'
	gh = GitHub(repo_url)	
	dependents = gh.dependents()
	assert len(dependents) >= 8
