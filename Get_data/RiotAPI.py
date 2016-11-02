import Consts
import requests
import time

class RiotAPI(object):
	def __init__(self, api_key):
		self.api_key = api_key

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
				print "HTTPS request error. Wait for 30 seconds..."
				time.sleep(30)
		return response.json()

	def get_summoner_by_name(self, name):
		api_url = Consts.URL['summoner_by_name'].format(
			version=Consts.VERSIONS['summoner'],
			names=name)
		# names using , seperate, limit is 40 at once.
		return self._request(api_url)

	def get_featured_games(self):
		args = {'api_key': self.api_key}
		response = requests.get(Consts.URL['featured_games'], params=args)
		return response.json()

	def get_summoner_games(self, summoner_id):
		api_url = Consts.URL['summoner_games'].format(
			version=Consts.VERSIONS['summoner_games'],
			id=summoner_id)
		return self._request(api_url)