import os
import simplejson as json
import mysql.connector
from flask import jsonify
from models.Player import Player
from models.Team import Team
from dotenv import load_dotenv
load_dotenv()

APP_ACCESS_DB_HOST = os.getenv("APP_ACCESS_DB_HOSTNAME")
APP_ACCESS_DB_USERNAME = os.getenv("APP_ACCESS_DB_USERNAME")
APP_ACCESS_DB_PASSWORD = os.getenv("APP_ACCESS_DB_PASSWORD")
APP_ACCESS_DB_DATABASE = os.getenv("APP_ACCESS_DB_DATABASE")
APP_ACCESS_DB_PORT = int(os.getenv("APP_ACCESS_DB_PORT"))

PARAM_QUERY_FAILED = "parameterized query failed {}"
CONNECTION_CLOSED = "MySQL connection is closed"

import logging
logger = logging.getLogger('app')


def createConnection(): 
	return mysql.connector.connect(
			host = APP_ACCESS_DB_HOST,
			user = APP_ACCESS_DB_USERNAME,
			password = APP_ACCESS_DB_PASSWORD,
			database = APP_ACCESS_DB_DATABASE
		)

def getDatabaseSchema(): 
	connection = createConnection()
	cursor = connection.cursor()
	dbSchemaQuery = f"""SELECT table_name FROM information_schema.tables WHERE table_schema = '{APP_ACCESS_DB_DATABASE}';"""
	cursor.execute(dbSchemaQuery)
	tables = cursor.fetchall()
	strippedTables = [tableName[0] for tableName in tables]
	schema = {}
	for tableName in strippedTables:
		if tableName == 'playerstats_old':
			continue

		tableSchemaQuery = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{tableName}' AND table_schema = '{APP_ACCESS_DB_DATABASE}';"
		print('tableschema: ', tableSchemaQuery)
		cursor.execute(tableSchemaQuery)
		columnNames = cursor.fetchall()
		strippedColumns = [columnName[0] for columnName in columnNames]
		schema[tableName] = [column for column in strippedColumns]

	connection.close()
	print('final table schema:', schema)
	return schema

# General sql select queries
def selectAllPlayersNotInStats():
	# selectQuery = """SELECT * FROM players WHERE id NOT IN (SELECT playerId FROM playerstats_updated);"""

	selectQuery = """SELECT * 
					FROM players 
					WHERE id > (SELECT MAX(playerId) FROM playerstats_updated);"""

	data = executeSelectQuery(selectQuery, [])
	return [Player(player['id'], player['name'], player['baseballReferenceUrl'], player['pitcher']) for player in data['items']]

def selectAllPlayers():
	selectQuery = """ select * from players """
	
	data = executeSelectQuery(selectQuery, [])
	return [Player(player['id'], player['name'], player['baseballReferenceUrl'], player['pitcher']) for player in data['items']]

def selectAllTeams():
	selectQuery = """ select * from teams """
	
	data = executeSelectQuery(selectQuery, [])
	return [Team(team['id'], team['name'], team['baseballReferenceUrl']) for team in data['items']]

def updatePlayerAsPitcher(playerId):
	updateQuery = f"""UPDATE players SET pitcher = 1 WHERE id = {playerId} """
	executeQuery(updateQuery, [])

# Helper methods for working with data
def createTableColumnsString(dbColumns, newTable: bool):
	if newTable == True: 
		return ", ".join([' '.join([column['columnName'], column['dataType']]) for column in dbColumns if column['dataType']])
	else: 
		
		return ", ".join([column['columnName'] for column in dbColumns if 'dataType' in column])

def createValuesString(dbData):
	formattedValues = ["NULL" if value == "" or value is None else f"'{value}'" for value in dbData]
	return ", ".join(formattedValues)

def createInsertQuery(table, id, idSpecifier, columnDefinitionsSring, valueDefinitionsString):
		return f"""INSERT INTO {table} ({idSpecifier}, {columnDefinitionsSring})
					VALUES ({id}, {valueDefinitionsString})"""

def createTable(tableName, columnDefinitionsSring, primaryKeyId):
	dropTableQuery = f"DROP TABLE IF EXISTS {tableName};"
	executeQuery(dropTableQuery, [])

	createTableQuery = f"""
		CREATE TABLE {tableName} (
			{primaryKeyId} INT PRIMARY KEY, {columnDefinitionsSring}
		);
	"""
	print(createTableQuery)

	executeQuery(createTableQuery, [])





def executeQuery(query, params):
	if not isinstance(params, list):
		params = [params]

	connection = createConnection()
	cursor = connection.cursor()

	try:
		cursor.execute(query, params)
		connection.commit()
		return {'success': True, 'affected_rows': cursor.rowcount} 

	except mysql.connector.Error as err:
		print(f"Error: {err}")
		connection.rollback()  # Rollback in case of error
		return jsonify({'success': False, 'error': str(err)}), 500

	finally:
	# Ensure resources are cleaned up
		if cursor:
			cursor.close()
		if connection and connection.is_connected():
			connection.close()


def executeAddSQL(insert_tuple, INSERT_SQL):
	try:  
		with mysql.connector.connect(
			host = APP_ACCESS_DB_HOST,
			user = APP_ACCESS_DB_USERNAME,
			password = APP_ACCESS_DB_PASSWORD,
			database = APP_ACCESS_DB_DATABASE,
			port = APP_ACCESS_DB_PORT
		) as connection:
			with connection.cursor(prepared=True) as cursor:
				print('SQL_UTILITY ', INSERT_SQL, insert_tuple)
				cursor.execute(INSERT_SQL, insert_tuple)
				connection.commit()
				cursor.close() 
			
			return jsonify({'success': True}), 200
	
	except mysql.connector.Error as error:
		print(PARAM_QUERY_FAILED.format(error))
		logger.debug("ERROR executeAddSQL() %s", INSERT_SQL)
		logger.debug("Tuple %s", insert_tuple)
		logger.debug("Exception ", exc_info=True)
		return jsonify({'success': False, 'message': error.msg}), 500
	
	finally:
		if connection.is_connected():
			connection.cursor().close()
			connection.close()
			print(CONNECTION_CLOSED)
			print()
	
def executeSelectQuery(query, params):
	items = []

	if not isinstance(params, list):
		params = [params]
	try:
		connection = createConnection()
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

# Delete
def execute_delete_sql(update_delete_tuple, sql):
	try:
		with mysql.connector.connect(
			host = APP_ACCESS_DB_HOST,
			user = APP_ACCESS_DB_USERNAME,
			password = APP_ACCESS_DB_PASSWORD,
			database = APP_ACCESS_DB_DATABASE,
			port = APP_ACCESS_DB_PORT,
		) as connection:
					   
			with connection.cursor(prepared=True) as cursor:
				cursor.execute(sql, update_delete_tuple)
				connection.commit()
				cursor.close()

		return jsonify({'success': True}), 200        
				
	except mysql.connector.Error as error:
		print(PARAM_QUERY_FAILED.format(error))
		logger.debug("ERROR executeUpdateDeleteSql() %s", sql)
		logger.debug("Tuple %s", update_delete_tuple)
		logger.debug("Exception ", exc_info=True)
		
		return jsonify({'success': False, 'message': error.msg}), 500
   
	finally:
		if connection.is_connected():
			connection.cursor().close()
			connection.close()
			print(CONNECTION_CLOSED)
			print()

# Update, or Insert if missing
def execute_update_insert_sql(tuple, update_sql, insert_sql):
	result_success = False

	try:
		with mysql.connector.connect(
			host = APP_ACCESS_DB_HOST,
			user = APP_ACCESS_DB_USERNAME,
			password = APP_ACCESS_DB_PASSWORD,
			database = APP_ACCESS_DB_DATABASE,
			port = APP_ACCESS_DB_PORT,
		) as connection:
			  
			with connection.cursor(prepared=True) as cursor:
				cursor.execute(update_sql, tuple)
				logger.debug("SQL: %s --result rows: %s", update_sql, cursor.rowcount)

				if (cursor.rowcount == 0):
					cursor.execute(insert_sql, tuple)
					logger.debug("SQL: %s --result rows: %s", insert_sql, cursor.rowcount)

				if (cursor.rowcount != 1):
					logger.error("ERROR executeUpdateInsertSql() %s", insert_sql)
				else:
					result_success = True
				
				connection.commit()
				cursor.close()
		
		numericResponse = 200
		if (result_success != True):
			numericResponse = 500

		return jsonify({'success': result_success}), numericResponse
				
	except mysql.connector.Error as error:
		print(PARAM_QUERY_FAILED.format(error))
		logger.debug("ERROR executeUpdateInsertSql()")
		logger.debug("Tuple %s", tuple)
		logger.debug("Exception ", exc_info=True)
		
		return jsonify({'success': False, 'message': error.msg}), 500
   
	finally:
		if connection.is_connected():
			connection.cursor().close()
			connection.close()
			print(CONNECTION_CLOSED)
			print()
	   
