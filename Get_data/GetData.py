from RiotAPI import RiotAPI
import time
import datetime

class GetData(object):
	def __init__(self, api):
		self.api = api
		self.summoner_ids = []
		self.games = {}
		self.p_game = 0
		self.p_summoner = 0
		print "Initializing, please wait..."
		self._first_run()

	def _first_run(self):
		summoner_games = self._get_from_api(1)
		names = []
		for game in summoner_games["gameList"]:
			if game["gameMode"] != "CLASSIC":
				continue
			for player in game["participants"]:
				if player["summonerName"] not in names:
					names.append(player["summonerName"])
		for name in names:
			id = self._get_from_api(2, [name])
			for key, value in id.items():
				if value["id"] not in self.summoner_ids:
					self.summoner_ids.append(value["id"])
			time.sleep(1)

	def _get_from_api(self, mode, params=[]):
		while True:
			if mode == 1:
				result = self.api.get_featured_games()
			elif mode == 2:
				result = self.api.get_summoner_by_name(params[0])
			elif mode == 3:
				result = self.api.get_summoner_games(params[0])

			if "status" in result:
				if result["status"]["status_code"] == 429:
					print "Over rate limit. Wait for 30 seconds..."
					time.sleep(30)
				else:
					print "Unknow Error. Code: " + str(result["status"]["status_code"]) +". Wait for 10 seconds..."
					time.sleep(10)
			else:
				return result
	
	def run(self):
		while True:
			if self.p_summoner == len(self.summoner_ids):
				self._first_run()
			self._get_summoner_games()
			self.p_summoner += 1
			if len(self.games) - self.p_game >= 10:
				print "Write to file..."
				self._write_to_file()
				print "Done! 10 new games have been write to file."
			time.sleep(1)

	def _get_summoner_games(self):
		summoner_games = self._get_from_api(3, [self.summoner_ids[self.p_summoner]])
		for game in summoner_games["games"]:
			if game["gameId"] in self.games:
				continue
			if game["gameMode"] != "CLASSIC" or game["gameType"] != "MATCHED_GAME":
				continue
			if len(game["fellowPlayers"]) != 9:
				continue
			wins = []
			losses = []
			team_id = game["teamId"]
			is_win = game["stats"]["win"]
			if is_win:
				wins.append(game["championId"])
			else:
				losses.append(game["championId"])
			for player in game["fellowPlayers"]:
				if player["summonerId"] not in self.summoner_ids:
					self.summoner_ids.append(player["summonerId"])
				if player["teamId"] == team_id:
					if is_win:
						wins.append(player["championId"])
					else:
						losses.append(player["championId"])
				else:
					if is_win:
						losses.append(player["championId"])
					else:
						wins.append(player["championId"])
			self.games[game["gameId"]] = wins + losses
			print "1 new game record! Already have " + str(len(self.games)) + " games."

	def _write_to_file(self):
		now = datetime.datetime.now()
		filename = now.strftime("%Y-%m-%d")+".txt"
		data = ""
		for i in range(10):
			gameid, combo = self.games.items()[self.p_game]
			data += str(gameid)
			for id in combo:
				data += "\t" + str(id)
			data += "\n"
			self.p_game += 1
		with open(filename, "a") as f:
			f.write(data)



