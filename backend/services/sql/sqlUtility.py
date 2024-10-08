import os
import simplejson as json
import mysql.connector
from flask import jsonify
from models.Player import Player
from models.Team import Team
# may need to add in :
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from utils.customLogging import logErrors
from dotenv import load_dotenv
load_dotenv()

APP_ACCESS_DB_HOST = os.getenv("APP_ACCESS_DB_HOSTNAME")
APP_ACCESS_DB_USERNAME = os.getenv("APP_ACCESS_DB_USERNAME")
APP_ACCESS_DB_PASSWORD = os.getenv("APP_ACCESS_DB_PASSWORD")
APP_ACCESS_BASEBALL_DB = os.getenv("APP_ACCESS_BASEBALL_DB")
APP_ACCESS_FITNESS_DB = os.getenv("APP_ACCESS_FITNESS_DB")

APP_ACCESS_DB_PORT = int(os.getenv("APP_ACCESS_DB_PORT"))

PARAM_QUERY_FAILED = "parameterized query failed {}"
CONNECTION_CLOSED = "MySQL connection is closed"

import logging
logger = logging.getLogger('app')


def createConnection(database): 
	return mysql.connector.connect(
			host = APP_ACCESS_DB_HOST,
			user = APP_ACCESS_DB_USERNAME,
			password = APP_ACCESS_DB_PASSWORD,
			database = database
		)

def getDatabaseSchema(): 
	"""
		Retrieve the database schema, including table names and their corresponding columns.

		This function connects to the database, queries for all tables within the specified 
		schema, and retrieves the column names for each table, excluding specific tables 
		as needed.

		Returns:
			dict: A dictionary where keys are table names and values are lists of column names.
    """
	connection = createConnection()
	cursor = connection.cursor()
	dbSchemaQuery = f"""SELECT table_name FROM information_schema.tables WHERE table_schema = '{APP_ACCESS_BASEBALL_DB}';"""
	cursor.execute(dbSchemaQuery)
	tables = cursor.fetchall()
	strippedTables = [tableName[0] for tableName in tables]
	ignoredTables = ['playerstats_old', 'changelog']
	schema = {}
	for tableName in strippedTables:
		if tableName in ignoredTables:
			continue

		tableSchemaQuery = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{tableName}' AND table_schema = '{APP_ACCESS_BASEBALL_DB}';"
		cursor.execute(tableSchemaQuery)
		columnNames = cursor.fetchall()
		strippedColumns = [columnName[0] for columnName in columnNames]
		schema[tableName] = [column for column in strippedColumns]

	connection.close()
	print('final table schema:', schema)
	return schema

# Helper methods for working with data
def createTableColumnsString(dbColumns: list, newTable: bool) -> str:
	"""
		Generate a string representation of database column definitions.

		This function constructs a formatted string for SQL column definitions 
		based on the provided list of columns. The format varies depending on 
		whether a new table is being created or an existing table is being modified.

		Args:
			dbColumns (list): * A list of dictionaries, each containing 'columnName' and 'dataType'.
			newTable (bool): * A flag indicating whether the columns are for a new table.

		Returns:
			str: A comma-separated string of column definitions for SQL statements.
    """
	if newTable == True: 
		return ", ".join([' '.join([column['columnName'], column['dataType']]) for column in dbColumns if column['dataType']])
	else: 
		
		return ", ".join([column['columnName'] for column in dbColumns if 'dataType' in column])

def createValuesString(dbData: list):
	"""
		Generate a formatted string of values for SQL insert statements.

		This function takes a list of data values and formats them for use 
		in an SQL query. Empty strings and None values are converted to 
		"NULL", while all other values are enclosed in single quotes.

		Args:
			dbData (list): * A list of values to be formatted for SQL.

		Returns:
			str: A comma-separated string of formatted values ready for an SQL query.
    """
    
	formattedValues = ["NULL" if value == "" or value is None else f"'{value}'" for value in dbData]
	return ", ".join(formattedValues)

def createInsertQuery(table: str, id: int, idSpecifier: str, columnDefinitionsSring: str, valueDefinitionsString: str) -> str:
	return f"""INSERT INTO {table} ({idSpecifier}, {columnDefinitionsSring})
				VALUES ({id}, {valueDefinitionsString})"""

def createUpdateQuery(table: str, id: int, idSpecifier: str, columnDefinitionsSring: str, valueDefinitionsString: str):
	updateQuery = f"""
			REPLACE INTO {table} ({idSpecifier}, {columnDefinitionsSring})
			VALUES ({id}, {valueDefinitionsString});
		"""
	
	executeQuery(APP_ACCESS_BASEBALL_DB, updateQuery, [])

def createTable(tableName: str, columnDefinitionsSring: str, primaryKeyId: str):
	dropTableQuery = f"DROP TABLE IF EXISTS {tableName};"
	executeQuery(APP_ACCESS_BASEBALL_DB, dropTableQuery, [])

	createTableQuery = f"""
		CREATE TABLE {tableName} (
			{primaryKeyId} INT PRIMARY KEY, {columnDefinitionsSring}
		);
	"""

	executeQuery(APP_ACCESS_BASEBALL_DB, createTableQuery, [])

def exportToDatabase(tableName: str, id: int, idSpecifier: str, dbColumns: list, dbData: list, createNewDatabaseTable: bool, loggingName: str):
	# remove the keys of each object and get just the values
	cleanedColumns = [list(column.values())[0] for column in dbColumns]

	columnDefinitionsSring = createTableColumnsString(cleanedColumns, createNewDatabaseTable)
	valueDefinitionsString = createValuesString(dbData)

	if createNewDatabaseTable == True:	
		createTable(tableName, columnDefinitionsSring, idSpecifier)

	insertQuery = createInsertQuery(tableName, id, idSpecifier, columnDefinitionsSring, valueDefinitionsString) 

	try:
		executeQuery(APP_ACCESS_BASEBALL_DB, insertQuery, [])
	except Exception as e:
		failReason = f"SQL query: \n{insertQuery}\n failed for {loggingName} {str(e)}"
		logErrors(failReason)


# General sql select queries
def selectAllPlayersNotInStats() -> list[Player]:
	# selectQuery = """SELECT * FROM players WHERE id NOT IN (SELECT playerId FROM playerstats_updated);"""

	selectQuery = """SELECT * 
					FROM players 
					WHERE id > (SELECT MAX(playerId) FROM playerstats_updated);"""

	data = executeSelectQuery(APP_ACCESS_BASEBALL_DB, selectQuery, [])
	return [Player(player['id'], player['name'], player['baseballReferenceUrl'], player['pitcher']) for player in data['items']]

def selectAllPlayers() -> list[Player]:
	selectQuery = """ select * from players """
	
	data = executeSelectQuery(APP_ACCESS_BASEBALL_DB, selectQuery, [])
	return [Player(player['id'], player['name'], player['baseballReferenceUrl'], player['pitcher']) for player in data['items']]

def selectAllTeams() -> list[Team]:
	selectQuery = """ select * from teams """
	
	data = executeSelectQuery(APP_ACCESS_BASEBALL_DB, selectQuery, [])
	return [Team(team['id'], team['name'], team['baseballReferenceUrl']) for team in data['items']]

def updatePlayerAsPitcher(playerId: int):
	updateQuery = f"""UPDATE players SET pitcher = 1 WHERE id = {playerId} """
	executeQuery(APP_ACCESS_BASEBALL_DB, updateQuery, [])


def executeQuery(database, query, params):
	if not isinstance(params, list):
		params = [params]

	connection = createConnection(database)
	cursor = connection.cursor()

	try:
		cursor.execute(query, params)
		# If the query is a SELECT query, fetch the results
		if query.strip().upper().startswith("SELECT"):
			results = cursor.fetchall()  # Fetch all results
			return {'success': True, 'data': results}
		connection.commit()
		affectedRows = cursor.rowcount

		return {'success': True, 'affectedRows': affectedRows} 

	except mysql.connector.Error as err:
		print(f"Error: {err}")
		connection.rollback()  # Rollback in case of error
		# logChange(operationType, tableName, query, 'failure', str(err))
		return jsonify({'success': False, 'error': str(err)}), 500

	finally:
	# Ensure resources are cleaned up
		if cursor:
			cursor.close()
		if connection and connection.is_connected():
			connection.close()


# def executeAddSQL(insert_tuple, INSERT_SQL):
# 	try:  
# 		with mysql.connector.connect(
# 			host = APP_ACCESS_DB_HOST,
# 			user = APP_ACCESS_DB_USERNAME,
# 			password = APP_ACCESS_DB_PASSWORD,
# 			database = APP_ACCESS_DB_DATABASE,
# 			port = APP_ACCESS_DB_PORT
# 		) as connection:
# 			with connection.cursor(prepared=True) as cursor:
# 				print('SQL_UTILITY ', INSERT_SQL, insert_tuple)
# 				cursor.execute(INSERT_SQL, insert_tuple)
# 				connection.commit()
# 				cursor.close() 
			
# 			return jsonify({'success': True}), 200
	
# 	except mysql.connector.Error as error:
# 		print(PARAM_QUERY_FAILED.format(error))
# 		logger.debug("ERROR executeAddSQL() %s", INSERT_SQL)
# 		logger.debug("Tuple %s", insert_tuple)
# 		logger.debug("Exception ", exc_info=True)
# 		return jsonify({'success': False, 'message': error.msg}), 500
	
# 	finally:
# 		if connection.is_connected():
# 			connection.cursor().close()
# 			connection.close()
# 			print(CONNECTION_CLOSED)
# 			print()
	
def executeSelectQuery(database, query, params):
	items = []

	# if not isinstance(params, list):
	# 	params = [params]
	try:
		connection = createConnection(database)
		cursor = connection.cursor(buffered=True)

		cursor.execute(query, params)
		rows = cursor.fetchall()

		# Create a list of dictionaries from the result set
		items = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in rows]

		return {'status': 'success', 'items': items}

	except mysql.connector.Error as err:
		print(f"Error: {err}")
		return {'status': 'fail', 'error': str(err), 'items': items}

	finally:
		# Ensure resources are cleaned up
		if cursor:
			cursor.close()
		if connection and connection.is_connected():
			connection.close()

# # Delete
# def execute_delete_sql(update_delete_tuple, sql):
# 	try:
# 		with mysql.connector.connect(
# 			host = APP_ACCESS_DB_HOST,
# 			user = APP_ACCESS_DB_USERNAME,
# 			password = APP_ACCESS_DB_PASSWORD,
# 			database = APP_ACCESS_DB_DATABASE,
# 			port = APP_ACCESS_DB_PORT,
# 		) as connection:
					   
# 			with connection.cursor(prepared=True) as cursor:
# 				cursor.execute(sql, update_delete_tuple)
# 				connection.commit()
# 				cursor.close()

# 		return jsonify({'success': True}), 200        
				
# 	except mysql.connector.Error as error:
# 		print(PARAM_QUERY_FAILED.format(error))
# 		logger.debug("ERROR executeUpdateDeleteSql() %s", sql)
# 		logger.debug("Tuple %s", update_delete_tuple)
# 		logger.debug("Exception ", exc_info=True)
		
# 		return jsonify({'success': False, 'message': error.msg}), 500
   
# 	finally:
# 		if connection.is_connected():
# 			connection.cursor().close()
# 			connection.close()
# 			print(CONNECTION_CLOSED)
# 			print()

# # Update, or Insert if missing
# def execute_update_insert_sql(tuple, update_sql, insert_sql):
# 	result_success = False

# 	try:
# 		with mysql.connector.connect(
# 			host = APP_ACCESS_DB_HOST,
# 			user = APP_ACCESS_DB_USERNAME,
# 			password = APP_ACCESS_DB_PASSWORD,
# 			database = APP_ACCESS_DB_DATABASE,
# 			port = APP_ACCESS_DB_PORT,
# 		) as connection:
			  
# 			with connection.cursor(prepared=True) as cursor:
# 				cursor.execute(update_sql, tuple)
# 				logger.debug("SQL: %s --result rows: %s", update_sql, cursor.rowcount)

# 				if (cursor.rowcount == 0):
# 					cursor.execute(insert_sql, tuple)
# 					logger.debug("SQL: %s --result rows: %s", insert_sql, cursor.rowcount)

# 				if (cursor.rowcount != 1):
# 					logger.error("ERROR executeUpdateInsertSql() %s", insert_sql)
# 				else:
# 					result_success = True
				
# 				connection.commit()
# 				cursor.close()
		
# 		numericResponse = 200
# 		if (result_success != True):
# 			numericResponse = 500

# 		return jsonify({'success': result_success}), numericResponse
				
# 	except mysql.connector.Error as error:
# 		print(PARAM_QUERY_FAILED.format(error))
# 		logger.debug("ERROR executeUpdateInsertSql()")
# 		logger.debug("Tuple %s", tuple)
# 		logger.debug("Exception ", exc_info=True)
		
# 		return jsonify({'success': False, 'message': error.msg}), 500
   
# 	finally:
# 		if connection.is_connected():
# 			connection.cursor().close()
# 			connection.close()
# 			print(CONNECTION_CLOSED)
# 			print()
	   
