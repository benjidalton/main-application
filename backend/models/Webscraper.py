from bs4 import BeautifulSoup
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# custom imports
import services.sql.sqlUtility as sqlUtility
from utils.columnDefinitions import allColumns
from utils.customLogging import logErrors
from utils.helperFunctions import prettyPrintHtml, handleEscapeCharaceters

class WebScraper:
	def __init__(self):
		self.chromeOptions = Options()
		self.chromeOptions.add_argument('--ignore-certificate-errors')
		self.chromeOptions.add_argument('--allow-insecure-localhost')
		self.chromeOptions.add_argument('--disable-logging')
		self.chromeOptions.add_argument('--log-level=3')
		self.chromeOptions.add_argument("--headless-old")
		self.sleepTime = 0 

		self.driver = None
		self.htmlContent = None

	def startDriver(self):
		"""Initialize the selenium webdriver"""
		if self.driver is None:
			self.driver = webdriver.Chrome(options=self.chromeOptions)
	
	def closeDriver(self):
		"""Close the selenium webdriver if it's running"""
		if self.driver is not None:
			self.driver.quit()
			self.driver = None

	def getHtmlContent(self, url: str):
		self.startDriver()
		self.driver.get(url)
		if self.sleepTime != 0:
			print(f'sleeping for {self.sleepTime}s to load content')
			time.sleep(self.sleepTime)

		htmlContent = self.driver.page_source
		self.htmlContent = BeautifulSoup(htmlContent, 'html.parser')
		
	def determinePlayerPosition(self):
		"""
			Determine if a player is a Pitcher based on HTML content.

			Args:
				soup (BeautifulSoup): * The BeautifulSoup object representing the parsed HTML document.

			Returns:
				bool: True if the player is a Pitcher, False otherwise.
		"""
		meta = self.htmlContent.find('div', {'id': 'meta'})
		positionText = meta.find('p').text.strip()
		position = positionText.replace('Position:', '').strip()
		return True if position == 'Pitcher' else False

	def getTable(self, tableFindParam: tuple, loggingName: str):
		"""
			Retrieve a specific table from the HTML soup based on given parameters.

			Args:
				tableFindParam (tuple): * Parameters to locate the table (e.g., (tag, attributes)).
				driver (webdriver.Chrome): * The Selenium WebDriver instance for potential further actions (not used in this function).
				soup (BeautifulSoup): * The BeautifulSoup object representing the HTML document.
				loggingName: * Identifier for logging purposes.

			Returns:
				BeautifulSoup or None: The found table as a BeautifulSoup object, or None if not found.
		"""
		dataTable = None
		dataTable = self.htmlContent.find(*tableFindParam)

		# prettyPrintHtml(dataTable, f"table{tableIdx}")
		if dataTable is None:
			failReason = f'No 2024 table found for these params {tableFindParam}.'
			logErrors(failReason)

		return dataTable
	
	def stripDataFromTablesByParam(self, tableFindParam: str, definingDataStats: list[str], desiredDataStatValues: list[str], loggingName: str) -> list:
		"""
			Extracts and processes data from HTML tables based on specified parameters.

			Args:
				tableFindParam: * Parameter to locate the target table.
				driver: * Selenium WebDriver instance for browser automation.
				soup: * BeautifulSoup object for parsing HTML content.
				definingDataStats: * List of statistics to define the data structure.
				desiredDataStatValues: * List of values to extract from the table.
				loggingName: * Name used for logging errors or info messages.

			Returns:
				allTablesData: List containing processed data from the table(s).
		"""
		
		allTablesData = []
		tableValues = None

		try: 
			dataTable = self.getTable(tableFindParam, loggingName)
		except ValueError as ve:
			logErrors(str(ve).format(loggingName))

		if dataTable != None:
			# prettyPrintHtml(dataTable, f"datatable{tableIdx + 1}")
			try:
				tableValues = self.stripDataFromTableRows(dataTable, definingDataStats, desiredDataStatValues, loggingName)
			except ValueError as ve:
				logErrors(str(ve).format(loggingName))

			# prettyPrintHtml(tableValues, f"tablesvalues{tableIdx + 1}")
			if tableValues != None:
				allTablesData.append(tableValues)

		return allTablesData

	def stripDataFromTableRows(dataTable: BeautifulSoup, definingDataStats: list[str], desiredDataStatValues: list[str], loggingName: str) -> list:
		"""
			Extract relevant data from the rows of an HTML table.

			This function processes the rows of a given HTML table, filtering out unnecessary rows 
			and extracting specified statistical data. It organizes the data into a structured format 
			for further processing.

			Args:
				dataTable (BeautifulSoup): * The HTML table element containing player statistics.
				definingDataStats (list): * A list of statistics that define the data structure.
				desiredDataStatValues (list): * The specific values to include in the extraction.
				loggingName (str): * A name used for logging errors.

			Returns:
				list: A list of dictionaries containing the extracted data for each relevant row.
		"""
		
		rows = dataTable.find('tbody').find_all('tr')
		allValues = []
		definingValue = None
		filteredRows = [row for row in rows if 'minors_table' not in row.get('class', [])]
		try: 
			for idx, row in enumerate(filteredRows):
				rowData = {}
				row = row.find_all(['td', 'th']) 
				for cell in row:
					dataStat = cell.get('data-stat')
					if dataStat: 

						## this correctly finds the team value in the table.
						## will be used to handle cases where player was traded during season
						# if dataStat == "team_ID":
						# 	teamValue = cell.text.strip()
						# 	if teamValue == 'TOT':

						if dataStat in definingDataStats:
							definingValue = cell.text.strip()
							if definingValue not in desiredDataStatValues:
								continue
							
						if definingValue not in rowData:
							rowData[definingValue] = {}

						rowData[definingValue][dataStat] = cell.text.strip() 
				if rowData:  # Add row data if it's not empty
					allValues.append(rowData)
		except ValueError as ve:
			logErrors(str(ve).format(loggingName))

		return allValues

	def getPlayersDataTables(self):
		"""
			Fetch and process player data tables from a website and update the database.

			The function retrieves player statistics from a website, processes the data,
			and inserts it into a database. It also checks for players' positions and handles
			cases where players may have been traded during the season.

			Steps:
				1. Retrieve players not in the statistics database.
				2. Loop through each player, fetching their data and determining their position.
				3. Depending on the position, fetch the appropriate data table.
				4. Extract relevant data, clean it, and prepare for database insertion.
				5. Handle exceptions and log errors where necessary.
		"""
		# things to work on:
		## handle players who were traded during the season 
		### need to look for row where data-stat: team_ID = 'TOT'
		### currently it gets all rows, leading to import errors into db

		players = sqlUtility.selectAllPlayersNotInStats()
		desiredDataStatValues = ['2024']
		definingDataStats = ['year_ID']
		loggingName = 'all-players'
		createNewDatabaseTable = False
		tableName = 'playerstats_updated'
		idSpecifier = 'playerId'

		for idx, player in enumerate(players):
			print(f'\n\nBeginning new search: ({idx + 1}/{len(players)})\nName: {player.name} ID: {player.id}')
			
			self.getHtmlContent(player.baseballReferenceUrl)

			playerIsPitcher = self.determinePlayerPosition()
			if playerIsPitcher:
				sqlUtility.updatePlayerAsPitcher(player.id)
				tableFindParam = ('table', {'id': 'pitching_standard'})
			else: 
				tableFindParam = ('table', {'id': 'batting_standard'})
			
			try:
				allTables = self.stripDataFromTablesByParam(tableFindParam, definingDataStats, desiredDataStatValues, loggingName)
			except Exception() as e:
				logErrors(str(e).format(loggingName))


			def extractMatchingItems():
				"""Extract matching items based on desired data statistics."""
				return [
					obj[val] for table in allTables
					for obj in table
					for val in desiredDataStatValues  # Iterate through each value in desiredDataStatValue
					if val in obj and obj[val]['year_ID'] in val  # Check if the year matches 
				]
			
			matchingItems = extractMatchingItems()
			
			if len(matchingItems) == 0: 
				print(f'No matching data for: {player.name}. Proceeding to next entry.')
				self.closeDriver()
				continue

			def prepareDatabaseEntries():		
				"""Prepare database entries from matching items."""	
				ignoreColumns = ['year_ID', 'age', 'team_ID', 'lg_ID', 'award_summary', 'G']
				repeatColumns =  ['H', 'R', 'HR', 'BB', 'IBB', 'SO', 'HBP']
				dbColumns = []
				dbData = []

				for matchingItem in matchingItems:
					for key, value in matchingItem.items():
						if key not in ignoreColumns:
							if key in repeatColumns and playerIsPitcher:
								key += "Allowed"  # Modify key for repeat columns

							# Ensure we get the column data from allColumns
							columnData = allColumns.get(key)
							if columnData:  # Only add if the column exists in allColumns
								dbColumns.append({key: columnData})
								dbData.append(value)
				
				return dbColumns, dbData
			
			dbColumns, dbData = prepareDatabaseEntries()

			sqlUtility.exportToDatabase(tableName, player.id, idSpecifier, dbColumns, dbData, createNewDatabaseTable, loggingName)

			self.closeDriver()
			
	def getTeamDataTables(self):
		teams = sqlUtility.selectAllTeams()
		
		desiredDataStatValues = [team.name for team in teams]
		definingDataStats = ['team_name']
		tableParams = [('table', {'id': 'teams_standard_batting'}), ('table', {'id': 'teams_standard_pitching'})]
		loggingName = 'all-teams'
		createNewDatabaseTable = False
		tableName = 'teamstats'
		idSpecifier = 'teamId'

		self.getHtmlContent('https://www.baseball-reference.com/leagues/majors/2024.shtml')
		
		for team in teams:
			dbColumns = []
			dbData = []
			for tableParam in tableParams:
				
				try:
					allTables = self.stripDataFromTablesByParam(tableParam, definingDataStats, desiredDataStatValues, loggingName)
				except Exception() as e:
					logErrors(str(e).format(loggingName))


				def extractMatchingItems():
					"""Extract matching items based on desired data statistics."""
					return [
						obj[team.name] for table in allTables
						for obj in table
						for definingDataStat in definingDataStats
						if team.name in obj and obj[team.name][definingDataStat] == team.name  
					]

				matchingItems = extractMatchingItems()

				def prepareDatabaseEntries():
					ignoreColumns = ['team_name', 'G', 'LOB']
					repeatColumns = ['H', 'R', 'HR', 'BB', 'IBB', 'SO', 'HBP']
					isPitchingTable = 'pitching' in tableParam[1]['id']

					for matchingItem in matchingItems:
						for key, value in matchingItem.items():
							if key not in ignoreColumns:
								if key in repeatColumns and isPitchingTable:
									key += "Allowed"  # Modify key for repeat columns

								# Ensure we get the column data from allColumns
								columnData = allColumns.get(key)
								if columnData:  # Only add if the column exists in allColumns
									dbColumns.append({key: columnData})
									dbData.append(value)

				dbColumns, dbData = prepareDatabaseEntries()

				if not dbColumns or not dbData:
					failReason = f"No valid data found for {loggingName}."
					logErrors(failReason)
					self.closeDriver()

			sqlUtility.exportToDatabase(tableName, team.id, idSpecifier, dbColumns, dbData, createNewDatabaseTable, loggingName)

		self.closeDriver()

	def getTeamSchedule(self):
		teamScheduleUrl = "2024-schedule-scores.shtml"
		# teams = sqlUtility.selectAllTeams()

		tableParam = ('table', {'id': 'teams_schedule'})
		loggingName = 'team-schedule'
		createNewDatabaseTable = False
		tableName = 'teamschedule'
		idSpecifier = 'teamId'

		definingDataStats = ['team_game']

		self.getHtmlContent('https://www.baseball-reference.com/teams/PHI/2024-schedule-scores.shtml')

		# for team in teams:
		dbColumns = []
		dbData = []
			
		try:
			dataTable = self.getTable(tableParam, loggingName)
		except Exception() as e:
			logErrors(str(e).format(loggingName))

		print('data table: ', dataTable)


		rows = dataTable.find('tbody').find_all('tr')
		allValues = []
		definingValue = None
		filteredRows = [row for row in rows if 'thead' not in row.get('class', [])]
		try: 
			for idx, row in enumerate(filteredRows):
				rowData = {}
				row = row.find_all(['td', 'th']) 
				for htmlElement in row:
					dataStatElement = htmlElement.get('data-stat')
					if dataStatElement: 
						if dataStatElement == 'date_game':
							dataValue = dataStatElement['csk']
						elif dataStatElement in ['winning_pitcher', 'losing_pitcher', 'opp_ID']:
							dataValue = dataStatElement.find('a')['href']

						else:
							dataValue = htmlElement.text.strip() 

						## this correctly finds the team value in the table.
						## will be used to handle cases where player was traded during season
						# if dataStat == "team_ID":
						# 	teamValue = cell.text.strip()
						# 	if teamValue == 'TOT':

						if dataStatElement in definingDataStats:
							definingValue = htmlElement.text.strip()
							# if definingValue not in desiredDataStatValues:
							# 	continue
							
						if definingValue not in rowData:
							rowData[definingValue] = {}

						rowData[definingValue][dataStatElement] = dataValue
				if rowData:  # Add row data if it's not empty
					allValues.append(rowData)
		except ValueError as ve:
			logErrors(str(ve).format(loggingName))









		def extractMatchingItems():
			"""Extract matching items based on desired data statistics."""
			return [
				obj[team.name] for table in allTables
				for obj in table
				for definingDataStat in definingDataStats
				if team.name in obj and obj[team.name][definingDataStat] == team.name  
			]

		matchingItems = extractMatchingItems()

		def prepareDatabaseEntries():
			# ignore columns looks for values of 'data-stat' in each element
			ignoreColumns =  ['time_of_game', 'reschedule', 'win_loss_streak' 'boxscore', 'team_id', 'CLI']

			for matchingItem in matchingItems:
				for key, value in matchingItem.items():
					if key not in ignoreColumns:
						# Ensure we get the column data from allColumns
						columnData = allColumns.get(key)
						if columnData:  # Only add if the column exists in allColumns
							dbColumns.append({key: columnData})
							dbData.append(value)

		dbColumns, dbData = prepareDatabaseEntries()

		if not dbColumns or not dbData:
			failReason = f"No valid data found for {loggingName}."
			logErrors(failReason)
			self.closeDriver()

	sqlUtility.exportToDatabase(tableName, team.id, idSpecifier, dbColumns, dbData, createNewDatabaseTable, loggingName)

	self.closeDriver()

webScraper = WebScraper()