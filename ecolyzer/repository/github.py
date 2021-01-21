import requests
from bs4 import BeautifulSoup
import time


class GitHub():
	"""GitHub"""

	base_url = 'https://github.com/'

	def __init__(self, repo_url: str):
		self._repo_url = repo_url

	def dependents(self, stars: int=0, forks: int=0):
		url = f'{self._repo_url}/network/dependents'
		deps = []

		while url:
			r = requests.get(url)
			soup = BeautifulSoup(r.content, 'html.parser')
			data = [
			   	self._create_dependent(t)
			    for t in soup.find_all('div', {'class': 'Box-row'})\
			    	if (self._stars(t) >= stars) and (self._forks(t) >= forks)
			]
			if len(data) > 0:
				deps += data
			 
			url = self._next_url(soup)
			self._rate_limit_constraint()
		
		self._remove_self_dependency(deps)

		return deps 

	def remove_duplicated(self, dependents, by_stars: bool=False, by_forks: bool=False):
		deps_dict = {}
		for d in dependents:
			if d.repo in deps_dict:
				a = d
				b = deps_dict[d.repo]
				if by_forks and (a.forks > b.forks):
					deps_dict[d.repo] = a
				elif by_stars and (a.stars > b.stars):
					deps_dict[d.repo] = a
			else:
				deps_dict[d.repo] = d
		return deps_dict.values()

	#TODO: repo depends on self - problem
	def _remove_self_dependency(self, dependents): 
		for i in range(len(dependents)):
			if dependents[i].url == self._repo_url:
				dependents.pop(i)
				return self._remove_self_dependency(dependents)

	def _create_dependent(self, tag):
		user_org = self._user_or_org(tag)
		repo = self._repository(tag)
		stars = self._stars(tag)
		forks = self._forks(tag)
		return Dependent(user_org, repo, stars, forks)

	def _user_or_org(self, tag):
		return tag.find('a', {'data-repository-hovercards-enabled':''}).string
		
	def _repository(self, tag):
		return tag.find('a', {'data-hovercard-type':'repository'}).string

	def _stars(self, tag):
		stars_text = tag.find('svg', {'class':'octicon octicon-star'}).parent.text
		return self._to_number(stars_text)

	def _forks(self, tag):
		forks_text = tag.find('svg', {'class':'octicon octicon-repo-forked'}).parent.text
		return self._to_number(forks_text)		

	def _to_number(self, text):
		return int(''.join(filter(str.isdigit, text)))

	def _next_url(self, soup):
		anchors = soup.find('div', {'class':'paginate-container'}).find_all('a')
		if len(anchors) > 0:
			if anchors[-1].string == 'Next':
				return anchors[-1]['href']
		return None

	def _rate_limit_constraint(self):
		time.sleep(1)


class Dependent():
	"""Dependent"""
	def __init__(self, user_org: str, repo: str, stars: int, forks: int):
		self._user_org = user_org
		self._repo = repo
		self._stars = stars
		self._forks = forks

	@property
	def user_or_org(self) -> str:
		return self._user_org

	@property
	def repo(self):
		return self._repo
	
	@property
	def stars(self) -> int:
		return self._stars

	@property
	def forks(self) -> int:
		return self._forks		
	
	@property
	def url(self) -> str:
		return f'{GitHub.base_url}{self._user_org}/{self._repo}'
	

		