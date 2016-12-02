from RiotAPI import RiotAPI
from GetData import GetData
import csv

def get_champions(api):
	result = api.get_champions()["champions"]
	champions = {}
	for champion in result:
		champions[champion["id"]] = [champion["freeToPlay"]]
	for id in champions.keys():
		detail = api.get_champion_by_id(id)
		champions[id].append(detail['name'])
	return champions

def get_champions_spells(api):
	params = {'champData':'spells'}
	result = api.get_champions()["champions"]
	champions = {}
	for champion in result:
		champions[champion["id"]] = []
	for id in champions.keys():
		detail = api.get_champion_by_id(id, params)
		for spell in detail['spells']:
			champions[id].append([spell['name'], spell['description']])
	return 

def get_champions_prop(api):
	params = {'champData':'stats'}
	result = api.get_champions()["champions"]
	champions = {}
	for champion in result:
		champions[champion["id"]] = []
	for id in champions.keys():
		detail = api.get_champion_by_id(id, params)
		s = detail['stats']
		champions[id].append([s['hp'], s['mp'], s['attackdamage'], s['armor'], s['hpperlevel'], s['mpperlevel'], s['attackdamageperlevel'], s['armorperlevel']])
	return champions

def write_to_csv(data, filename):
	with open(filename, 'wb') as csv_file:
		writer = csv.writer(csv_file)
		for key, value in data.items():
			row = [key]
			for v in value:
				if isinstance(v, list):
					for i in v:
						row.append(i)
				else:
					row.append(v)
			writer.writerow(row)

def write_spells(data, filename):
	with open(filename, 'wb') as csv_file:
		writer = csv.writer(csv_file)
		for key, value in data.items():
			for v in value:
				row = [key]
				for i in v:
					row.append(i)
				writer.writerow(row)

def main():
	api = RiotAPI("RGAPI-ac961b5c-4740-4fd0-9f9b-585ec0b78924")
	#write_to_csv(get_champions(api), "Champions.csv")
	#write_spells(get_champions_spells(api), "Spells.csv")
	write_to_csv(get_champions_prop(api), "Props.csv")

if __name__ == '__main__':
	main();