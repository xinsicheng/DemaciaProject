import Consts
import requests
import time

class RiotAPI(object):
	def __init__(self, api_key):
		#self.api_key = api_key
		self.api_key = Consts.API_KEYS[0]
		self.key_index = 0

	def change_key(self):
		self.key_index = (self.key_index + 1) % 10
		self.api_key = Consts.API_KEYS[self.key_index]

	def _request(self, api_url, params={}):
		args = {'api_key': self.api_key}
		for key, value in params.items():
			if key not in args:
				args[key] = value
		while True:
			try:
				response = requests.get(
					Consts.URL['base'].format(
						url=api_url),
					params=args)
				break
			except:
				print "HTTPS request error. Wait for 10 seconds..."
				time.sleep(10)
		return response.json()

	def _request_url(self, url, params={}):
		args = {'api_key': self.api_key}
		for key, value in params.items():
			if key not in args:
				args[key] = value
		while True:
			try:
				response = requests.get(url, params=args)
				break
			except:
				print "HTTPS request error. Wait for 10 seconds..."
				time.sleep(5)
		return response.json()

	def get_summoner_by_name(self, name):
		api_url = Consts.URL['summoner_by_name'].format(
			version=Consts.VERSIONS['summoner'],
			names=name)
		# names using , seperate, limit is 40 at once.
		return self._request(api_url)

	def get_champions(self):
		api_url = Consts.URL['all_champions'].format(
			version=Consts.VERSIONS['champion'])
		return self._request(api_url)

	def get_champion_by_id(self, champion_id, params={}):
		url = Consts.URL['champion_by_id'].format(id=champion_id)
		return self._request_url(url, params)

	def get_featured_games(self):
		args = {'api_key': self.api_key}
		response = requests.get(Consts.URL['featured_games'], params=args)
		return response.json()

	def get_summoner_games(self, summoner_id):
		api_url = Consts.URL['summoner_games'].format(
			version=Consts.VERSIONS['summoner_games'],
			id=summoner_id)
		return self._request(api_url)

	def get_match_by_id(self, id):
		api_url = Consts.URL['match'].format(
			version=Consts.VERSIONS['match'],
			matchid=id)
		return self._request(api_url)

	def get_items(self, params={}):
		url = Consts.URL['items']
		return self._request_url(url, params)