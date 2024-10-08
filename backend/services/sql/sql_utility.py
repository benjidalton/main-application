import os
import simplejson as json
import mysql.connector
from flask import jsonify
from models.Player import Player
from models.Team import Team
# may need to add in :
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.utils.custom_logging import logErrors
from dotenv import load_dotenv
load_dotenv()

APP_ACCESS_DB_HOST = os.getenv("APP_ACCESS_DB_HOSTNAME")
APP_ACCESS_DB_USERNAME = os.getenv("APP_ACCESS_DB_USERNAME")
APP_ACCESS_DB_PASSWORD = os.getenv("APP_ACCESS_DB_PASSWORD")
APP_ACCESS_BASEBALL_DB = os.getenv("APP_ACCESS_BASEBALL_DB")
APP_ACCESS_FITNESS_DB = os.getenv("APP_ACCESS_FITNESS_DB")

APP_ACCESS_DB_PORT = int(os.getenv("APP_ACCESS_DB_PORT"))

db_user = os.getenv("APP_ACCESS_DB_USERNAME")
db_pass = os.getenv("APP_ACCESS_DB_PASSWORD")
db_host = os.getenv("APP_ACCESS_DB_HOSTNAME")
db_name = os.getenv("APP_ACCESS_DB_DATABASE")
db_port = os.getenv("APP_ACCESS_DB_PORT")

# Construct the database URL
DATABASE_URI = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

# Create an engine
engine = create_engine(DATABASE_URI)

PARAM_QUERY_FAILED = "parameterized query failed {}"
CONNECTION_CLOSED = "MySQL connection is closed"

import logging
logger = logging.getLogger('app')


def create_connection(database): 
	return mysql.connector.connect(
			host = APP_ACCESS_DB_HOST,
			user = APP_ACCESS_DB_USERNAME,
			password = APP_ACCESS_DB_PASSWORD,
			database = database
		)

def get_database_schema(): 
	"""
		Retrieve the database schema, including table names and their corresponding columns.

		This function connects to the database, queries for all tables within the specified 
		schema, and retrieves the column names for each table, excluding specific tables 
		as needed.

		Returns:
			dict: A dictionary where keys are table names and values are lists of column names.
    """
	connection = create_connection()
	cursor = connection.cursor()
	dbSchemaQuery = f"""SELECT table_name FROM information_schema.tables WHERE table_schema = '{APP_ACCESS_BASEBALL_DB}';"""
	cursor.execute(dbSchemaQuery)
	tables = cursor.fetchall()
	strippedTables = [table_name[0] for table_name in tables]
	ignoredTables = ['playerstats_old', 'changelog']
	schema = {}
	for table_name in strippedTables:
		if table_name in ignoredTables:
			continue

		tableSchemaQuery = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' AND table_schema = '{APP_ACCESS_BASEBALL_DB}';"
		cursor.execute(tableSchemaQuery)
		columnNames = cursor.fetchall()
		strippedColumns = [columnName[0] for columnName in columnNames]
		schema[table_name] = [column for column in strippedColumns]

	connection.close()
	print('final table schema:', schema)
	return schema

# Helper methods for working with data
def create_table_columns_string(db_columns: list, newTable: bool) -> str:
	"""
		Generate a string representation of database column definitions.

		This function constructs a formatted string for SQL column definitions 
		based on the provided list of columns. The format varies depending on 
		whether a new table is being created or an existing table is being modified.

		Args:
			db_columns (list): * A list of dictionaries, each containing 'columnName' and 'dataType'.
			newTable (bool): * A flag indicating whether the columns are for a new table.

		Returns:
			str: A comma-separated string of column definitions for SQL statements.
    """
	if newTable == True: 
		return ", ".join([' '.join([column['columnName'], column['dataType']]) for column in db_columns if column['dataType']])
	else: 
		
		return ", ".join([column['columnName'] for column in db_columns if 'dataType' in column])

def create_values_string(db_data: list):
	"""
		Generate a formatted string of values for SQL insert statements.

		This function takes a list of data values and formats them for use 
		in an SQL query. Empty strings and None values are converted to 
		"NULL", while all other values are enclosed in single quotes.

		Args:
			db_data (list): * A list of values to be formatted for SQL.

		Returns:
			str: A comma-separated string of formatted values ready for an SQL query.
    """
    
	formattedValues = ["NULL" if value == "" or value is None else f"'{value}'" for value in db_data]
	return ", ".join(formattedValues)

def create_insert_query(table: str, id: int, id_specifier: str, column_defs_string: str, value_defs_string: str) -> str:
	return f"""INSERT INTO {table} ({id_specifier}, {column_defs_string})
				VALUES ({id}, {value_defs_string})"""

def create_update_query(table: str, id: int, id_specifier: str, column_defs_string: str, value_defs_string: str):
	updateQuery = f"""
			REPLACE INTO {table} ({id_specifier}, {column_defs_string})
			VALUES ({id}, {value_defs_string});
		"""
	
	execute_query(APP_ACCESS_BASEBALL_DB, updateQuery, [])

def create_table(table_name: str, column_defs_string: str, primaryKeyId: str):
	dropTableQuery = f"DROP TABLE IF EXISTS {table_name};"
	execute_query(APP_ACCESS_BASEBALL_DB, dropTableQuery, [])

	create_tableQuery = f"""
		CREATE TABLE {table_name} (
			{primaryKeyId} INT PRIMARY KEY, {column_defs_string}
		);
	"""

	execute_query(APP_ACCESS_BASEBALL_DB, create_tableQuery, [])

def export_to_db(table_name: str, id: int, id_specifier: str, db_columns: list, db_data: list, create_new_db_table: bool, logging_name: str):
	# remove the keys of each object and get just the values
	cleaned_columns = [list(column.values())[0] for column in db_columns]

	column_defs_string = create_table_columns_string(cleaned_columns, create_new_db_table)
	value_defs_string = create_values_string(db_data)

	if create_new_db_table == True:	
		create_table(table_name, column_defs_string, id_specifier)

	insertQuery = create_insert_query(table_name, id, id_specifier, column_defs_string, value_defs_string) 

	try:
		execute_query(APP_ACCESS_BASEBALL_DB, insertQuery, [])
	except Exception as e:
		failReason = f"SQL query: \n{insertQuery}\n failed for {logging_name} {str(e)}"
		logErrors(failReason)


# General sql select queries
def select_all_players_not_in_stats() -> list[Player]:
	# select_query = """SELECT * FROM players WHERE id NOT IN (SELECT playerId FROM playerstats_updated);"""

	select_query = """SELECT * 
					FROM players 
					WHERE id > (SELECT MAX(playerId) FROM playerstats_updated);"""

	data = execute_select_query(APP_ACCESS_BASEBALL_DB, select_query, [])
	return [Player(player['id'], player['name'], player['baseballReferenceUrl'], player['pitcher']) for player in data['items']]

def select_all_players() -> list[Player]:
	select_query = """ select * from players """
	
	data = execute_select_query(APP_ACCESS_BASEBALL_DB, select_query, [])
	return [Player(player['id'], player['name'], player['baseballReferenceUrl'], player['pitcher']) for player in data['items']]

def select_all_teams() -> list[Team]:
	select_query = """ select * from teams """
	
	data = execute_select_query(APP_ACCESS_BASEBALL_DB, select_query, [])
	return [Team(team['id'], team['name'], team['baseballReferenceUrl']) for team in data['items']]

def update_player_as_pitcher(playerId: int):
	updateQuery = f"""UPDATE players SET pitcher = 1 WHERE id = {playerId} """
	execute_query(APP_ACCESS_BASEBALL_DB, updateQuery, [])


def execute_query(database, query, params):
	if not isinstance(params, list):
		params = [params]

	connection = create_connection(database)
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
		# logChange(operationType, table_name, query, 'failure', str(err))
		return jsonify({'success': False, 'error': str(err)}), 500

	finally:
	# Ensure resources are cleaned up
		if cursor:
			cursor.close()
		if connection and connection.is_connected():
			connection.close()
	
def execute_select_query(database, query, params):
	items = []

	# if not isinstance(params, list):
	# 	params = [params]
	try:
		connection = create_connection(database)
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
	   
