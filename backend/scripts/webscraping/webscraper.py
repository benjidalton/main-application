import requests
from requests.exceptions import RequestException
import string
from bs4 import BeautifulSoup

import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import sql.sqlUtility as sqlUtility
# from sql.sqlUtility import executeQuery, executeSelectQuery
from models.Player import Player
from models.Team import Team
from .scrapingTables import allColumns
from customLogging import logErrors

chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--allow-insecure-localhost')
chrome_options.add_argument('--disable-logging')
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument("--headless-old")
sleepTime = 0 

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

def prettyPrintHtml(htmlContent, fileName, mode = 'w'):
	with open('./htmlFiles/' + fileName + '.html', mode, encoding='utf-8') as file:
		file.write(str(htmlContent))


def stripDataFromTablesById(tableFindParam, driver: webdriver.Chrome, soup: BeautifulSoup, definingDataStats, desiredDataStatValues, loggingName):

	allTablesData = []
	# for tableIdx, tableId in enumerate(tableIds):
	tableValues = None

	try: 
		dataTable = getTable(tableFindParam, driver, soup, loggingName)
	except ValueError as ve:
		logErrors(str(ve).format(loggingName))
	

	if dataTable != None:
		# prettyPrintHtml(dataTable, f"datatable{tableIdx + 1}")
		try:
			tableValues = stripDataFromTableRows(dataTable, definingDataStats, desiredDataStatValues, loggingName)
		except ValueError as ve:
			logErrors(str(ve).format(loggingName))

		# prettyPrintHtml(tableValues, f"tablesvalues{tableIdx + 1}")
		if tableValues != None:
			allTablesData.append(tableValues)

	return allTablesData

def getTable(tableFindParam: tuple, driver: webdriver.Chrome, soup: BeautifulSoup, loggingName):
	dataTable = None

	dataTable = soup.find(*tableFindParam)

	# prettyPrintHtml(dataTable, f"table{tableIdx}")
	if dataTable is None:
		failReason = f'No 2024 table found for these params {tableFindParam}.'
		logErrors(failReason)

	return dataTable

def stripDataFromTableRows(dataTable: BeautifulSoup, definingDataStats, desiredDataStatValues, loggingName):
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

def determinePlayerPosition(soup: BeautifulSoup):
	meta = soup.find('div', {'id': 'meta'})
	positionText = meta.find('p').text.strip()
	position = positionText.replace('Position:', '').strip()
	return True if position == 'Pitcher' else False

def getTeamDataTables():
	items = sqlUtility.selectAllTeamsFromDb()
	desiredDataStatValues = [item.name for item in items]
	definingDataStats = ['team_name']
	tableIds = [('table', {'id': 'teams_standard_batting'}), ('table', {'id': 'teams_standard_pitching'})]
	loggingName = 'all-teams'
	createNewDatabaseTable = False
	newTableName = 'teamstats'
	insertTableName = 'teamstats'
	idSpecifier = 'teamId'

	driver, soup = None, None
	driver, soup = getHtmlContent('https://www.baseball-reference.com/leagues/majors/2024.shtml')

	try:
		allTables = stripDataFromTablesById(tableIds, driver, soup, definingDataStats, desiredDataStatValues, loggingName)
	except Exception() as e:
		logErrors(str(e).format(loggingName))
	

	ignoreColumns = ['team_name', 'G', 'LOB']
	repeatColumns = ['H', 'R', 'HR', 'BB', 'IBB', 'SO', 'HBP']

	for item in items:
		dbColumns = []
		dbData = []
		matchingItems = [
			obj[item.name] for table in allTables
			for obj in table
			for definingDataStat in definingDataStats
			if item.name in obj and obj[item.name][definingDataStat] == item.name  
		]


		for matchingItem in matchingItems:
			for key, value in matchingItem.items():
				if key not in ignoreColumns:
					if key in repeatColumns and any(item.get(key) for item in dbColumns):
						key += "Allowed"  # Modify key for repeat columns

					# Ensure we get the column data from allColumns
					columnData = allColumns.get(key)
					if columnData:  # Only add if the column exists in allColumns
						dbColumns.append({key: columnData})
						dbData.append(value)

		cleanedColumns = [list(column.values())[0] for column in dbColumns]

		if not dbColumns or not dbData:
			failReason = f"No valid data found for {loggingName}."
			logErrors(failReason)
			driver.close()

		columnDefinitionsSring = sqlUtility.createTableColumnsString(cleanedColumns, createNewDatabaseTable)
		valueDefinitionsString = sqlUtility.createValuesString(dbData)

		if createNewDatabaseTable == True:	
			sqlUtility.createTable(newTableName, columnDefinitionsSring, idSpecifier)
			break

		insertQuery = sqlUtility.createInsertQuery(insertTableName, item.id, idSpecifier, columnDefinitionsSring, valueDefinitionsString) 

		try:
			sqlUtility.executeQuery(insertQuery, [])
		except Exception as e:
			failReason = f"SQL query: \n{insertQuery}\n failed for {loggingName} {str(e)}"
			logErrors(failReason)

def getPlayersDataTables():
	# things to work on:
	## handle players who were traded during the season 
	### need to look for row where data-stat: team_ID = 'TOT'
	### currently it gets all rows, leading to import errors into db

	players = sqlUtility.selectAllPlayersNotInStats()
	desiredDataStatValues = ['2024']
	definingDataStats = ['year_ID']
	# tableIds = [('table', {'id': 'batting_standard'}), ('table', {'id': 'pitching_standard'})]
	loggingName = 'all-players'
	createNewDatabaseTable = False
	newTableName = 'playerstats_updated'
	insertTableName = 'playerstats_updated'
	idSpecifier = 'playerId'
	
	ignoreColumns = ['year_ID', 'age', 'team_ID', 'lg_ID', 'award_summary', 'G']
	repeatColumns =  ['H', 'R', 'HR', 'BB', 'IBB', 'SO', 'HBP']

	# for player in players:
	for idx, player in enumerate(players):
		print(f'\n\nBeginning new search: ({idx + 1}/{len(players)})\nName: {player.name} ID: {player.id}')
		driver, soup = None, None
		driver, soup = getHtmlContent(player.baseballReferenceUrl)

		playerIsPitcher = determinePlayerPosition(soup)
		if playerIsPitcher:
			sqlUtility.updatePlayerAsPitcher(player.id)
		print(f"{player.name} is a pitcher: {playerIsPitcher}")

		tableFindParam = ('table', {'id': 'pitching_standard'}) if playerIsPitcher else ('table', {'id': 'batting_standard'})

		try:
			allTables = stripDataFromTablesById(tableFindParam, driver, soup, definingDataStats, desiredDataStatValues, loggingName)
		except Exception() as e:
			logErrors(str(e).format(loggingName))

		matchingItems = [
			obj[val] for table in allTables
			for obj in table
			for val in desiredDataStatValues  # Iterate through each value in desiredDataStatValue
			if val in obj and obj[val]['year_ID'] in val  # Check if the year matches
			  
		]
		
		if len(matchingItems) == 0: 
			print(f'No matching data for: {player.name}. Proceeding to next entry.')
			driver.close()
			continue

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

		cleanedColumns = [list(column.values())[0] for column in dbColumns]

		columnDefinitionsSring = sqlUtility.createTableColumnsString(cleanedColumns, createNewDatabaseTable)
		valueDefinitionsString = sqlUtility.createValuesString(dbData)

		if createNewDatabaseTable == True:	
			sqlUtility.createTable(newTableName, columnDefinitionsSring, idSpecifier)
			break

		insertQuery = sqlUtility.createInsertQuery(insertTableName, player.id, idSpecifier, columnDefinitionsSring, valueDefinitionsString) 

		try:
			sqlUtility.executeQuery(insertQuery, [])
		except Exception as e:
			failReason = f"SQL query: \n{insertQuery}\n failed for {loggingName} {str(e)}"
			logErrors(failReason)
