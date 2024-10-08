from bs4 import BeautifulSoup
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# custom imports
import backend.services.sql.sql_utility as sql_utility
from backend.utils.column_definitions import allColumns
from backend.utils.custom_logging import log_errors
from backend.utils.helper_functions import pretty_print_html, handle_escape_characeters

class WebScraper:
	def __init__(self):
		self.chrome_options = Options()
		self.chrome_options.add_argument('--ignore-certificate-errors')
		self.chrome_options.add_argument('--allow-insecure-localhost')
		self.chrome_options.add_argument('--disable-logging')
		self.chrome_options.add_argument('--log-level=3')
		self.chrome_options.add_argument("--headless-old")
		self.sleepTime = 0 

		self.driver = None
		self.html_content = None

	def start_driver(self):
		"""Initialize the selenium webdriver"""
		if self.driver is None:
			self.driver = webdriver.Chrome(options=self.chrome_options)
	
	def close_driver(self):
		"""Close the selenium webdriver if it's running"""
		if self.driver is not None:
			self.driver.quit()
			self.driver = None

	def get_html_content(self, url: str):
		self.start_driver()
		self.driver.get(url)
		if self.sleepTime != 0:
			print(f'sleeping for {self.sleepTime}s to load content')
			time.sleep(self.sleepTime)

		html_content = self.driver.page_source
		self.html_content = BeautifulSoup(html_content, 'html.parser')
		
	def determine_player_position(self):
		"""
			Determine if a player is a Pitcher based on HTML content.

			Args:
				soup (BeautifulSoup): * The BeautifulSoup object representing the parsed HTML document.

			Returns:
				bool: True if the player is a Pitcher, False otherwise.
		"""
		meta = self.html_content.find('div', {'id': 'meta'})
		position_text = meta.find('p').text.strip()
		position = position_text.replace('Position:', '').strip()
		return True if position == 'Pitcher' else False

	def get_table(self, table_find_param: tuple, logging_name: str):
		"""
			Retrieve a specific table from the HTML soup based on given parameters.

			Args:
				table_find_param (tuple): * Parameters to locate the table (e.g., (tag, attributes)).
				driver (webdriver.Chrome): * The Selenium WebDriver instance for potential further actions (not used in this function).
				soup (BeautifulSoup): * The BeautifulSoup object representing the HTML document.
				logging_name: * Identifier for logging purposes.

			Returns:
				BeautifulSoup or None: The found table as a BeautifulSoup object, or None if not found.
		"""
		data_table = None
		data_table = self.html_content.find(*table_find_param)

		# prettyPrintHtml(data_table, f"table{tableIdx}")
		if data_table is None:
			fail_reason = f'No 2024 table found for these params {table_find_param}.'
			log_errors(fail_reason)

		return data_table
	
	def strip_data_from_tables_by_param(self, table_find_param: str, defining_data_stats: list[str], desired_data_stat_values: list[str], logging_name: str) -> list:
		"""
			Extracts and processes data from HTML tables based on specified parameters.

			Args:
				table_find_param: * Parameter to locate the target table.
				driver: * Selenium WebDriver instance for browser automation.
				soup: * BeautifulSoup object for parsing HTML content.
				defining_data_stats: * List of statistics to define the data structure.
				desired_data_stat_values: * List of values to extract from the table.
				logging_name: * Name used for logging errors or info messages.

			Returns:
				all_tables_data: List containing processed data from the table(s).
		"""
		
		all_tables_data = []
		table_values = None

		try: 
			data_table = self.get_table(table_find_param, logging_name)
		except ValueError as ve:
			log_errors(str(ve).format(logging_name))

		if data_table != None:
			# prettyPrintHtml(data_table, f"data_table{tableIdx + 1}")
			try:
				table_values = self.strip_data_from_table_rows(data_table, defining_data_stats, desired_data_stat_values, logging_name)
			except ValueError as ve:
				log_errors(str(ve).format(logging_name))

			# prettyPrintHtml(table_values, f"tablesvalues{tableIdx + 1}")
			if table_values != None:
				all_tables_data.append(table_values)

		return all_tables_data

	def strip_data_from_table_rows(data_table: BeautifulSoup, defining_data_stats: list[str], desired_data_stat_values: list[str], logging_name: str) -> list:
		"""
			Extract relevant data from the rows of an HTML table.

			This function processes the rows of a given HTML table, filtering out unnecessary rows 
			and extracting specified statistical data. It organizes the data into a structured format 
			for further processing.

			Args:
				data_table (BeautifulSoup): * The HTML table element containing player statistics.
				defining_data_stats (list): * A list of statistics that define the data structure.
				desired_data_stat_values (list): * The specific values to include in the extraction.
				logging_name (str): * A name used for logging errors.

			Returns:
				list: A list of dictionaries containing the extracted data for each relevant row.
		"""
		
		rows = data_table.find('tbody').find_all('tr')
		all_values = []
		defining_value = None
		filtered_rows = [row for row in rows if 'minors_table' not in row.get('class', [])]
		try: 
			for idx, row in enumerate(filtered_rows):
				row_data = {}
				row = row.find_all(['td', 'th']) 
				for cell in row:
					data_stat = cell.get('data-stat')
					if data_stat: 

						## this correctly finds the team value in the table.
						## will be used to handle cases where player was traded during season
						# if data_stat == "team_ID":
						# 	teamValue = cell.text.strip()
						# 	if teamValue == 'TOT':

						if data_stat in defining_data_stats:
							defining_value = cell.text.strip()
							if defining_value not in desired_data_stat_values:
								continue
							
						if defining_value not in row_data:
							row_data[defining_value] = {}

						row_data[defining_value][data_stat] = cell.text.strip() 
				if row_data:  # Add row data if it's not empty
					all_values.append(row_data)
		except ValueError as ve:
			log_errors(str(ve).format(logging_name))

		return all_values

	def get_players_data_tables(self):
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

		players = sql_utility.select_all_players_not_in_stats()
		desired_data_stat_values = ['2024']
		defining_data_stats = ['year_ID']
		logging_name = 'all-players'
		create_new_db_table = False
		table_name = 'playerstats_updated'
		id_specifier = 'playerId'

		for idx, player in enumerate(players):
			print(f'\n\nBeginning new search: ({idx + 1}/{len(players)})\nName: {player.name} ID: {player.id}')
			
			self.get_html_content(player.baseballReferenceUrl)

			player_is_pitcher = self.determine_player_position()
			if player_is_pitcher:
				sql_utility.update_player_as_pitcher(player.id)
				table_find_param = ('table', {'id': 'pitching_standard'})
			else: 
				table_find_param = ('table', {'id': 'batting_standard'})
			
			try:
				all_tables = self.strip_data_from_tables_by_param(table_find_param, defining_data_stats, desired_data_stat_values, logging_name)
			except Exception() as e:
				log_errors(str(e).format(logging_name))


			def extract_matching_items():
				"""Extract matching items based on desired data statistics."""
				return [
					obj[val] for table in all_tables
					for obj in table
					for val in desired_data_stat_values  # Iterate through each value in desireddata_statValue
					if val in obj and obj[val]['year_ID'] in val  # Check if the year matches 
				]
			
			matching_items = extract_matching_items()
			
			if len(matching_items) == 0: 
				print(f'No matching data for: {player.name}. Proceeding to next entry.')
				self.close_driver()
				continue

			def prepare_db_entries():		
				"""Prepare database entries from matching items."""	
				ignore_columns = ['year_ID', 'age', 'team_ID', 'lg_ID', 'award_summary', 'G']
				repeat_columns =  ['H', 'R', 'HR', 'BB', 'IBB', 'SO', 'HBP']
				db_columns = []
				db_data = []

				for matching_item in matching_items:
					for key, value in matching_item.items():
						if key not in ignore_columns:
							if key in repeat_columns and player_is_pitcher:
								key += "Allowed"  # Modify key for repeat columns

							# Ensure we get the column data from allColumns
							column_data = allColumns.get(key)
							if column_data:  # Only add if the column exists in allColumns
								db_columns.append({key: column_data})
								db_data.append(value)
				
				return db_columns, db_data
			
			db_columns, db_data = prepare_db_entries()

			sql_utility.export_to_db(table_name, player.id, id_specifier, db_columns, db_data, create_new_db_table, logging_name)

			self.close_driver()
			
	def get_team_data_tables(self):
		teams = sql_utility.select_all_teams()
		
		desired_data_stat_values = [team.name for team in teams]
		defining_data_stats = ['team_name']
		tableParams = [('table', {'id': 'teams_standard_batting'}), ('table', {'id': 'teams_standard_pitching'})]
		logging_name = 'all-teams'
		create_new_db_table = False
		table_name = 'teamstats'
		id_specifier = 'teamId'

		self.get_html_content('https://www.baseball-reference.com/leagues/majors/2024.shtml')
		
		for team in teams:
			db_columns = []
			db_data = []
			for table_param in tableParams:
				
				try:
					all_tables = self.strip_data_from_tables_by_param(table_param, defining_data_stats, desired_data_stat_values, logging_name)
				except Exception() as e:
					log_errors(str(e).format(logging_name))


				def extract_matching_items():
					"""Extract matching items based on desired data statistics."""
					return [
						obj[team.name] for table in all_tables
						for obj in table
						for definingdata_stat in defining_data_stats
						if team.name in obj and obj[team.name][definingdata_stat] == team.name  
					]

				matching_items = extract_matching_items()

				def prepare_db_entries():
					ignore_columns = ['team_name', 'G', 'LOB']
					repeat_columns = ['H', 'R', 'HR', 'BB', 'IBB', 'SO', 'HBP']
					is_pitching_table = 'pitching' in table_param[1]['id']

					for matching_item in matching_items:
						for key, value in matching_item.items():
							if key not in ignore_columns:
								if key in repeat_columns and is_pitching_table:
									key += "Allowed"  # Modify key for repeat columns

								# Ensure we get the column data from allColumns
								column_data = allColumns.get(key)
								if column_data:  # Only add if the column exists in allColumns
									db_columns.append({key: column_data})
									db_data.append(value)

				db_columns, db_data = prepare_db_entries()

				if not db_columns or not db_data:
					fail_reason = f"No valid data found for {logging_name}."
					log_errors(fail_reason)
					self.close_driver()

			sql_utility.export_to_db(table_name, team.id, id_specifier, db_columns, db_data, create_new_db_table, logging_name)

		self.close_driver()

	def get_team_schedule(self):
		teamScheduleUrl = "2024-schedule-scores.shtml"
		# teams = sqlUtility.selectAllTeams()

		table_param = ('table', {'id': 'teams_schedule'})
		logging_name = 'team-schedule'
		create_new_db_table = False
		table_name = 'teamschedule'
		id_specifier = 'teamId'

		defining_data_stats = ['team_game']

		self.get_html_content('https://www.baseball-reference.com/teams/PHI/2024-schedule-scores.shtml')

		# for team in teams:
		db_columns = []
		db_data = []
			
		try:
			data_table = self.get_table(table_param, logging_name)
		except Exception() as e:
			log_errors(str(e).format(logging_name))

		print('data table: ', data_table)


		rows = data_table.find('tbody').find_all('tr')
		all_values = []
		defining_value = None
		filtered_rows = [row for row in rows if 'thead' not in row.get('class', [])]
		try: 
			for idx, row in enumerate(filtered_rows):
				row_data = {}
				row = row.find_all(['td', 'th']) 
				for htmlElement in row:
					data_statElement = htmlElement.get('data-stat')
					if data_statElement: 
						if data_statElement == 'date_game':
							dataValue = data_statElement['csk']
						elif data_statElement in ['winning_pitcher', 'losing_pitcher', 'opp_ID']:
							dataValue = data_statElement.find('a')['href']

						else:
							dataValue = htmlElement.text.strip() 

						## this correctly finds the team value in the table.
						## will be used to handle cases where player was traded during season
						# if data_stat == "team_ID":
						# 	teamValue = cell.text.strip()
						# 	if teamValue == 'TOT':

						if data_statElement in defining_data_stats:
							defining_value = htmlElement.text.strip()
							# if defining_value not in desired_data_stat_values:
							# 	continue
							
						if defining_value not in row_data:
							row_data[defining_value] = {}

						row_data[defining_value][data_statElement] = dataValue
				if row_data:  # Add row data if it's not empty
					all_values.append(row_data)
		except ValueError as ve:
			log_errors(str(ve).format(logging_name))


		# def extract_matching_items():
		# 	"""Extract matching items based on desired data statistics."""
		# 	return [
		# 		obj[team.name] for table in all_tables
		# 		for obj in table
		# 		for definingdata_stat in defining_data_stats
		# 		if team.name in obj and obj[team.name][definingdata_stat] == team.name  
		# 	]

		# matching_items = extract_matching_items()

		# def prepare_db_entries():
		# 	# ignore columns looks for values of 'data-stat' in each element
		# 	ignore_columns =  ['time_of_game', 'reschedule', 'win_loss_streak' 'boxscore', 'team_id', 'CLI']

		# 	for matching_item in matching_items:
		# 		for key, value in matching_item.items():
		# 			if key not in ignore_columns:
		# 				# Ensure we get the column data from allColumns
		# 				column_data = allColumns.get(key)
		# 				if column_data:  # Only add if the column exists in allColumns
		# 					db_columns.append({key: column_data})
		# 					db_data.append(value)

		# db_columns, db_data = prepare_db_entries()

		# if not db_columns or not db_data:
		# 	fail_reason = f"No valid data found for {logging_name}."
		# 	log_errors(fail_reason)
		# 	self.close_driver()

		# sql_utility.exportToDatabase(table_name, team.id, id_specifier, db_columns, db_data, create_new_db_table, logging_name)

		# self.close_driver()

webScraper = WebScraper()