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


def test_dependents_forks():
	repo_url = 'https://github.com/apache/hadoop'
	gh = GitHub(repo_url)
	dependents = gh.dependents(forks=3)
	assert len(dependents) >= 7
	for dep in dependents:
		assert dep.stars >= 2
		assert dep.url is not None
		assert dep.url != repo_url
		assert dep.forks >= 0		


def test_dependents_without_next_url():
	repo_url = 'https://github.com/scribejava/scribejava'
	gh = GitHub(repo_url)	
	dependents = gh.dependents()
	assert len(dependents) >= 8

def test_remove_duplicated():
	repo_url = 'https://github.com/apache/hadoop'
	gh = GitHub(repo_url)
	dependents = gh.dependents()

	deps_dict = {}
	for d in dependents:
		deps_dict[d.repo] = d	

	deps_forks = gh.remove_duplicated(dependents, by_forks=True)
	assert len(deps_forks) == len(deps_dict)
	for d in deps_forks:
		assert d.url != None
		assert d.forks != None
		assert d.stars != None
	
	deps_stars = gh.remove_duplicated(dependents, by_stars=True)
	assert len(deps_stars) == len(deps_dict)
	for d in deps_stars:
		assert d.url != None
		assert d.forks != None
		assert d.stars != None

		