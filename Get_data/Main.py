from RiotAPI import RiotAPI
from GetData import GetData

def main():
	api = RiotAPI("RGAPI-ac961b5c-4740-4fd0-9f9b-585ec0b78924")
	gets = GetData(api)
	gets.run()
	#get_champions(api)

def get_champions(api):
	champions = api.get_champions()["champions"]
	i = 1
	result = ""
	for champion in champions:
		result += str(i) + "\t" + str(champion["id"]) + "\n"
		i += 1
	with open("champions.tsv", "a") as f:
		f.write(result)

if __name__ == '__main__':
	main()