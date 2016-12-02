from RiotAPI import RiotAPI
import time
import datetime

class GetData(object):
	def __init__(self, api):
		self.api = api
		self.summoner_ids = []
		self.game_ids = []
		self.games = []
		self.p_game = 0
		self.p_summoner = 0
		self.rank = ["UNRANKED", "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND", "MASTER", "CHALLENGER"]
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
		if len(names) > 40:
			names = names[0:40]
		ids = self._get_from_api(2, [",".join(names)])
		for name, id in ids.items():
			if id["id"] not in self.summoner_ids:
				self.summoner_ids.append(id["id"])
		time.sleep(1)

	def _get_from_api(self, mode, params=[]):
		while True:
			if mode == 1:
				result = self.api.get_featured_games()
			elif mode == 2:
				result = self.api.get_summoner_by_name(params[0])
			elif mode == 3:
				result = self.api.get_summoner_games(params[0])
			elif mode == 4:
				result = self.api.get_match_by_id(params[0])

			if "status" in result:
				if result["status"]["status_code"] == 429:
					self.api.change_key()
				else:
					if mode == 4 and result["status"]["status_code"] == 404:
						return ""
					print "Unknow Error. Code: " + str(result["status"]["status_code"]) +". Wait for 10 seconds..."
					print mode
					print params
					time.sleep(10)
			else:
				return result
	
	def run(self):
		while True:
			if self.p_summoner == len(self.summoner_ids):
				self._first_run()
			self._get_summoner_games()
			self.p_summoner += 1
			if len(self.game_ids) - self.p_game >= 10:
				self._write_to_file()
				print "Has written to file."
			time.sleep(1)

	def _get_summoner_games(self):
		summoner_games = self._get_from_api(3, [self.summoner_ids[self.p_summoner]])
		for game in summoner_games["games"]:
			if game["gameId"] in self.game_ids:
				continue
			if game["gameMode"] != "CLASSIC" or game["gameType"] != "MATCHED_GAME":
				continue
			if len(game["fellowPlayers"]) != 9:
				continue
			for player in game["fellowPlayers"]:
				if player["summonerId"] not in self.summoner_ids:
					self.summoner_ids.append(player["summonerId"])
			self._get_game_detail(game["gameId"])
		print "Already have " + str(len(self.game_ids)) + " games."

	def _get_game_detail(self, gameid):
		game = self._get_from_api(4, [gameid])
		if not game:
			return
		team1, team2, team1_rank, team2_rank, kill1, death1, assist1, kill2, death2, assist2 = [],[],[],[],[],[],[],[],[],[]
		win = -1
		for player in game["participants"]:
			if player["teamId"] == 100:
				win = [0] if player["stats"]["winner"] else [1]
				team1.append(player["championId"])
				rank = player["highestAchievedSeasonTier"] if player["highestAchievedSeasonTier"] else "UNRANKED"
				team1_rank.append(self.rank.index(rank))
				kill1.append(player["stats"]["kills"])
				death1.append(player["stats"]["deaths"])
				assist1.append(player["stats"]["assists"])
			else:
				team2.append(player["championId"])
				rank = player["highestAchievedSeasonTier"] if player["highestAchievedSeasonTier"] else "UNRANKED"
				team2_rank.append(self.rank.index(rank))
				kill2.append(player["stats"]["kills"])
				death2.append(player["stats"]["deaths"])
				assist2.append(player["stats"]["assists"])
		result = team1+team2+team1_rank+team2_rank+win+kill1+kill2+death1+death2+assist1+assist2
		self.game_ids.append(gameid)
		self.games.append(result)

	def _write_to_file(self):
		now = datetime.datetime.now()
		filename = now.strftime("%Y-%m-%d")+".txt"
		data = ""
		for i in range(len(self.games)):
			gameid = self.game_ids[self.p_game]
			data += str(gameid)
			combo = self.games[i]
			for id in combo:
				data += "\t" + str(id)
			data += "\n"
			self.p_game += 1
		with open(filename, "a") as f:
			f.write(data)
		self.games = []



