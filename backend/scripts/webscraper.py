import requests
from requests.exceptions import RequestException
import string
from bs4 import BeautifulSoup

import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from sql.sqlUtility import executeQuery, executeSelectQuery
from .scrapingTables import allColumns
from customLogging import logErrors

chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--allow-insecure-localhost')
chrome_options.add_argument('--disable-logging')
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument("--headless-old")
sleepTime = 0 




class Player:
	def __init__(self, id, name, baseballReferenceUrl) -> None:
		self.id = id
		self.name = name
		self.baseballReferenceUrl = baseballReferenceUrl
		self.currentTeam = ''

players: list[Player] = []



# helper functions
def handleEscapeCharaceters(strings): 
	if isinstance(strings, str): 
		return strings.replace("'", "''")
	return [substring.replace("'", "''") for substring in strings]

def getHtmlContent(url):
	driver = webdriver.Chrome(options=chrome_options)
	driver.get(url)
	if sleepTime != 0:
		print(f'sleeping for {sleepTime}s to load content')
		time.sleep(sleepTime)

	htmlContent = driver.page_source
	soup = BeautifulSoup(htmlContent, 'html.parser')
	return driver, soup

def fetchWithBackoff(url, retries=5):
	for i in range(retries):
		try:
			response = requests.get(url)
			response.raise_for_status()
			return response
		except requests.exceptions.HTTPError as e:
			if response.status_code == 429:
				waitTime = 2 ** i  # Exponential backoff
				print(f"429 error received. Waiting for {waitTime} seconds...")
				time.sleep(waitTime)
			else:
				print(f"HTTP error occurred: {e}")
				break
	return None

def prettyPrintHtml(htmlContent, fileName):
	with open('./htmlFiles/' + fileName, 'w', encoding='utf-8') as file:
		file.write(str(htmlContent))

def getTable(driver: webdriver.Chrome, soup: BeautifulSoup, playerName):
	tableId = 'batting_standard'
	dataTable = soup.find('tr', {'id': tableId + '.2024'})
	if dataTable is None:
		try:
			tableId = 'pitching_standard'
			dataTable = soup.find('tr', {'id': tableId + '.2024'})

			if dataTable is None:
				print(f"No standard table found for {playerName}. Skipping to next player.")
		except Exception as e:
			failReason = f"Error finding pitching table for {playerName}: {str(e)}"
			logErrors(failReason)
			driver.close()

	if dataTable is None or dataTable.get('id') not in ("batting_standard.2024", "pitching_standard.2024"):
		failReason = f'No 2024 table found for {playerName}. Continuing to next player.'
		logErrors(failReason)
		raise ValueError(f'No 2024 table found for {playerName}.')

	return dataTable, tableId


def selectAllPlayersNotInStats():
	selectQuery = """SELECT * FROM players WHERE id > (SELECT MAX(playerId) FROM stats) """
	# selectQuery = """SELECT *
	# 				FROM players p
	# 				WHERE NOT EXISTS (
	# 				    SELECT 1
	# 				    FROM stats s
	# 				    WHERE s.playerId = p.id
	# 				)"""
	data = executeSelectQuery(selectQuery, [])
	print('data: ', data)
	return [Player(player['id'], player['name'], player['baseballReferenceUrl']) for player in data['items']]

# webscraping and db manipulation
def getPlayers():
	   
	baseUrl = 'https://www.baseball-reference.com/players/{letter}/'
	id = 1659
	for letter in string.ascii_lowercase:
		if letter < 't':
			continue
		url = baseUrl.format(letter=letter)
		response = fetchWithBackoff(url)

		try:
			soup = BeautifulSoup(response.content, 'html.parser')


			playerTable = soup.find('div', {'id': 'div_players_'})
			if playerTable:
				# Active players are bolded
				activePlayers = playerTable.find_all('b')

				for active in activePlayers:
					player = active.find('a')  # Find the <a> tag inside the <b> tag
					if player:
						playerName = player.text
						playerUrl = f"https://www.baseball-reference.com{player['href']}"
						players.append(Player(id, playerName, playerUrl))

						id += 1
						
				print(f"Done fetching active players starting with: {letter.capitalize()}")
			else:
				print(f"Player table not found for letter: '{letter.capitalize()}'.")

		except RequestException as e:
			# Catch any request-related exceptions
			print(f"Error fetching data for letter '{letter.capitalize()}': {e}")
	
	
	insertQuery = """
		INSERT INTO players (id, name, teamId, baseballReferenceUrl)
		VALUES (%s, %s, %s, %s)
	"""
	for player in players:
		# Prepare the values to insert
		values = (player.id, player.name, None, player.baseballReferenceUrl) 
		response = executeQuery(insertQuery, values)
		print('response: ', response)
	

	return 

def allPlayersOnTeam(url):
	
	try:
		soup = getHtmlContent(url)

		teamNameTag = soup.find('h1').find('span')
		teamName = teamNameTag.find_next('span').text

		rosterTable = soup.find('table', {'id': 'appearances'})

		playerNames = []
		for row in rosterTable.find_all('tr')[0:]: 
			playerCell = row.find('th', {'data-stat': 'player'})
			if playerCell:
				playerName = playerCell.find_next('a').text  
				playerNames.append(playerName)
		
		escapedPlayerNames = handleEscapeCharaceters(playerNames) # handle cases like "Travis d'Arnaud"

		updatePlayerQuery = f""" UPDATE players 
							SET 
								players.teamId = (SELECT id FROM teams WHERE name = '{teamName}')
							WHERE 
       							 name IN ({', '.join(f"'{name}'" for name in escapedPlayerNames)}) 
   							 	"""
		
		updateTeamQuery = f"""UPDATE teams
							SET 
								baseballReferenceUrl = '{url}'
							WHERE 
								name = '{teamName}';"""
		queries = [updatePlayerQuery, updateTeamQuery]


		[executeQuery(query, []) for query in queries]

	except RequestException as e:
		# Catch any request-related exceptions
		print(f"Error fetching data: {e}")

def getPlayerTeams():
	# print(f'getting team info for: {player.name} using this url: {player.baseballReferenceUrl}')
	selectQuery = """ select * from players where players.teamId is null """
	data = executeQuery(selectQuery, [])

	players: list[Player] = [Player(player['id'], player['name'], player['baseballReferenceUrl']) for player in data['items']]
	numPlayers = len(players)
	failed = 0
	

	print(f'-- Beginning data import process of {numPlayers} entries--')
	for idx, player in enumerate(players):
		print(f'-- Importing process: {idx + 1}/{numPlayers} --')
		print(f'Current entry: {player.name}')
		teamName = ''
		try:
			
			driver, soup = getHtmlContent(player.baseballReferenceUrl)
			infoBox = soup.find('div', {'id': 'meta'})
		   
			if infoBox:
				teamInfo = infoBox.find(text="Team:")
				if teamInfo:
					teamName = teamInfo.find_next('a').text
				else:
					teamInfo = infoBox.find(text="Draft")
					if teamInfo:
						teamName = teamInfo.find_next('a').text
					else:
						print("No team information found on the page.")
						driver.close()
						continue
			else:
				print("Player meta box not found.")
			
			teamName = teamName if teamName != '' else None
			playerName = handleEscapeCharaceters(player.name)

			updatePlayerQuery = f""" UPDATE players 
								SET 
									players.teamId = (SELECT id FROM teams WHERE name = '{teamName}')
								WHERE 
	       							 name = '{playerName}'; 
							 	"""
			
			executeQuery(updatePlayerQuery, [])

			driver.close()

		except RequestException as e:
			# Catch any request-related exceptions
			failed += 1
			print(f"Error fetching data: {e}")
			continue
	
	print(f'Data import process completed! Success udpated {numPlayers - failed} entries.')



def getStandardBattingAndPitchingTables():
	while True:
		players: list[Player] = selectAllPlayersNotInStats()

		for idx, player in enumerate(players):
			print(f'\n\nBeginning new search: ({idx + 1}/{len(players)})\nName: {player.name} ID: {player.id}')
			try:
			
				driver, soup = None, None
				driver, soup = getHtmlContent(player.baseballReferenceUrl)
				
				try: 
					dataTable, tableId = getTable(driver, soup, player.name)
				except ValueError as ve:
					print(str(ve).format(player.name))  # Optional: print the error message 
					logErrors(str(ve).format(player.name))
					continue
				
				try:
					dataStatElements = dataTable.find_all(['th', 'td'])

					dataStatValues = {element.get('data-stat'): element.text for element in dataStatElements if element.get('data-stat')}
					ignoreColumns = ['year_ID', 'age', 'team_ID', 'lg_ID', 'award_summary']
					filteredDataStatValues = {key: value for key, value in dataStatValues.items() if key not in ignoreColumns}

					dbColumns = []
					dbData = []
					filteredDataStatValues
					for key in filteredDataStatValues.keys():
						data = filteredDataStatValues[key].strip()
						if key == "G":
							key = "gamesPlayedBatter" if tableId == 'batting_standard' else "gamesPlayedPitcher"
						
							if key in ['H', 'HR', 'BB', 'IBB', 'SO', 'HBP']:
								key = key if tableId == 'batting_standard' else key + "Allowed"

						dbColumns.append(allColumns[key])
						dbData.append(data)

					if not dbColumns or not dbData:
						failReason = f"No valid data found for {player.name}."
						logErrors(failReason)
						driver.close()
						continue

					# Prepare the SQL insert query
					columnDefinitions = [column['columnName'] for column in dbColumns if column['dataType']]
					columnsString = ", ".join(columnDefinitions)
					

					formattedValues = ["NULL" if value == "" or value is None else f"'{value}'" for value in dbData]
					valuesString = ", ".join(formattedValues)
					insertQuery = f"""INSERT INTO stats (playerId, {columnsString})
					                  VALUES ({player.id}, {valuesString})"""
					
					try:
						executeQuery(insertQuery, [])
					except Exception as e:
						failReason = f"SQL query: \n{insertQuery}\n failed for {player.name} - {player.id}: {str(e)}"
						logErrors(failReason)

				except Exception as e:
					failReason = f"Error while processing data for {player.name}: {str(e)}"
					logErrors(failReason)

			except Exception as e:
				failReason = f"Error initializing driver for {player.name}: {str(e)}"
				logErrors(failReason)

			finally:
				if driver:
					driver.close()


def createBattingDataBaseTable(dbColumns):
	decimalDataType = 'DECIMAL(5, 5)'
	intDataType = 'SMALLINT(10)'
	for column in dbColumns:
		if column['name'] in ['battingAverage', 'onBase', 'slugging', 'onBasePlusSlugging']:
			column['dataType'] = decimalDataType
		if column['name'] in ['gamesPlayed', 'plateAppearances', 'atBats', 'runsScored', 
								'hits', 'doubles', 'triples', 'homeRuns', 'runsBattedIn', 'stolenBases', 
								'caughtStealing', 'basesOnBalls', 'strikeouts', 'adjustedOPS', 'totalBases', 'doublePlaysGroundedInto', 
								'hitByPitch', 'sacrificeHits', 'sacrificeFlies', 'intentionalBasesOnBalls']:
			column['dataType'] = intDataType
		if column['name'] == 'position':
			column['dataType'] = 'TEXT(10)'
	print('dbColumns: ', dbColumns)

	# with open('output.txt', 'w') as file:
	# 	file.write('dbColumns: ' + str(dbColumns) + '\n')
	columnDefinitions = []
	for column in dbColumns:
		if column['dataType']:  # Check if dataType is not empty
			columnDefinitions.append(f"{column['name']} {column['dataType']}")

		# Join the column definitions into a single string for the CREATE TABLE statement
	columnsString = ",\n".join(columnDefinitions)
	
	# Create the SQL CREATE TABLE query
	createQuery = f"""
		CREATE TABLE stats (
			playerId INT PRIMARY KEY, {columnsString}
		);
	"""
	print(createQuery)

	executeQuery(createQuery, [])


def createPitchingDataBaseTable(dbColumns):
	decimalDataType = 'DECIMAL(5, 5)'
	intDataType = 'SMALLINT(10)'
	# for column in dbColumns:
	# 	if column['name'] in ['battingAverage', 'onBase', 'slugging', 'onBasePlusSlugging']:
	# 		column['dataType'] = decimalDataType
	# 	if column['name'] in ['gamesPlayed', 'plateAppearances', 'atBats', 'runsScored', 
	# 							'hits', 'doubles', 'triples', 'homeRuns', 'runsBattedIn', 'stolenBases', 
	# 							'caughtStealing', 'basesOnBalls', 'strikeouts', 'adjustedOPS', 'totalBases', 'doublePlaysGroundedInto', 
	# 							'hitByPitch', 'sacrificeHits', 'sacrificeFlies', 'intentionalBasesOnBalls']:
	# 		column['dataType'] = intDataType
	# 	if column['name'] == 'position':
	# 		column['dataType'] = 'TEXT(10)'
	# print('dbColumns: ', dbColumns)

	with open('output.txt', 'w') as file:
		file.write('dbColumns: ' + str(dbColumns) + '\n')
	columnDefinitions = []
	for column in dbColumns:
		if column['dataType']:  # Check if dataType is not empty
			columnDefinitions.append(f"{column['name']} {column['dataType']}")

		# Join the column definitions into a single string for the CREATE TABLE statement
	columnsString = ",\n".join(columnDefinitions)
	
	# Create the SQL CREATE TABLE query
	createQuery = f"""
		CREATE TABLE pitchingStats (
			playerId INT PRIMARY KEY, {columnsString}
		);
	"""
	print(createQuery)

	# sqlUtility.executeQuery(createQuery, [])


def scrapeTableData(statsInfo, tableData):
	dbColumns = []
	dbData = []
	for stat in statsInfo:
		findStat = stat['abbr']

		statNameSplitBySpace = stat['name'].split(' ')
		
		# if first index of list of sub strings for stat contains '-' 
		# split by '-', get lower case of first index, capitalize the second index and join the two
		# ex:  ['On-Base', 'Plus', 'Slugging'] => ['onBase', 'Plus', 'Slugging']
		firstPart = ''.join([statNameSplitBySpace[0].split('-')[0].lower(), statNameSplitBySpace[0].split('-')[1].capitalize()]) if '-' in statNameSplitBySpace[0] else statNameSplitBySpace[0].lower()
		secondPart = ''.join(statNameSplitBySpace[1:]) if len(statNameSplitBySpace) > 1 else None

		fullStatName = firstPart + secondPart if secondPart != None else firstPart

		if fullStatName == 'pos':
			fullStatName = 'position'
		if fullStatName == 'basesonBalls':
			fullStatName = 'basesOnBalls'
		if fullStatName == 'intentionalBasesonBalls':
			fullStatName = 'intentionalBasesOnBalls'

		formattedStatName = re.sub(r'[+%]$', '', fullStatName)
		dbColumns.append({'name': formattedStatName, 'dataType': ''})
		data = tableData.find('td', {'data-stat': findStat}).text
		if '*' in data:
			data = "'" + data.split('*')[1].split(r'/')[0] + "'" 
		dbData.append(data)
		print(f"Stat {formattedStatName} has a value of {data}")
	
	# formattedDbColumns = ', '.join(stat['name'] for stat in dbColumns)
	# formattedDbData =  ', '.join(value for value in dbData)

	# return formattedDbColumns, formattedDbData

	return dbColumns

def scrapeStatsInfo(columns):
	ignoreColumns = ['Year', 'Awards', 'Age', 'Tm', 'Lg']
	stats = []
	for column in columns:
		if column.attrs['aria-label'] in ignoreColumns:
			continue

		try:
			statName = column.attrs['aria-label']
		except KeyError: 
			statName = 'N/A'
		
		statAbbr = column.attrs['data-stat']
		
		# find all stat info in header of table
		stats.append({'name': statName, 'abbr': statAbbr})
	return stats

