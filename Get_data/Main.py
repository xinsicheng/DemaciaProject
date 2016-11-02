from RiotAPI import RiotAPI
from GetData import GetData

def main():
	api = RiotAPI("RGAPI-ac961b5c-4740-4fd0-9f9b-585ec0b78924")
	gets = GetData(api)
	gets.run()
	
if __name__ == '__main__':
	main()