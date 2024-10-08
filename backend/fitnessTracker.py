import os
import simplejson as json
import mysql.connector
from flask import jsonify
# may need to add in :
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from utils.customLogging import logErrors
from dotenv import load_dotenv
load_dotenv()

APP_ACCESS_DB_HOST = os.getenv("APP_ACCESS_DB_HOSTNAME")
APP_ACCESS_DB_USERNAME = os.getenv("APP_ACCESS_DB_USERNAME")
APP_ACCESS_DB_PASSWORD = os.getenv("APP_ACCESS_DB_PASSWORD")
APP_ACCESS_DB_DATABASE = 'fitness_tracker_db'
APP_ACCESS_DB_PORT = int(os.getenv("APP_ACCESS_DB_PORT"))
print(f"Host: {APP_ACCESS_DB_HOST}, User: {APP_ACCESS_DB_USERNAME}, Database: {APP_ACCESS_DB_DATABASE}, Port: {APP_ACCESS_DB_PORT}")

def createConnection(): 
	return mysql.connector.connect(
			host = APP_ACCESS_DB_HOST,
			user = APP_ACCESS_DB_USERNAME,
			password = APP_ACCESS_DB_PASSWORD,
			database = APP_ACCESS_DB_DATABASE
		)

def executeQuery(query, params):
	if not isinstance(params, list):
		params = [params]

	connection = createConnection()
	cursor = connection.cursor()
	try:
		cursor.execute(query, params)
		connection.commit()
		affectedRows = cursor.rowcount
		# Log success in the change_log table
		# logChange(operationType, tableName, query, 'success')

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

def createExerciseTable():
	
	tableName = 'exercise'
	dropTableQuery = f"DROP TABLE IF EXISTS {tableName};"

	result = executeQuery(dropTableQuery, [])
	if not result['success']:
		print("Failed to drop table:", result)
		return

	# date = date
	# name = name
	# muscleGroup = muscleGroup
	# sets = sets
	# reps = reps
	# weight = weight

	createTableQuery = f"""
		CREATE TABLE {tableName} (
			id INT AUTO_INCREMENT PRIMARY KEY, 
			name TEXT(50), 
			muscle_group_id INT
		);
	"""

	result = executeQuery(createTableQuery, [])
	if not result['success']:
		print("Failed to create table:", result)

def createMuscleGroupTable(): 

	tableName = 'muscle_group'
	dropTableQuery = f"DROP TABLE IF EXISTS {tableName};"

	result = executeQuery(dropTableQuery, [])
	if not result['success']:
		print("Failed to drop table:", result)
		return

	# date = date
	# name = name
	# muscleGroup = muscleGroup
	# sets = sets
	# reps = reps
	# weight = weight

	createTableQuery = f"""
		CREATE TABLE {tableName} (
			id INT AUTO_INCREMENT PRIMARY KEY, 
			name TEXT(50)
		);
	"""

	result = executeQuery(createTableQuery, [])
	if not result['success']:
		print("Failed to create table:", result)




def createMuscleGroups(): 
	insertQuery = """INSERT INTO muscle_group (name)
					VALUES 
						('biceps'), 
						('triceps'), 
						('shoulders'), 
						('chest'), 
						('back'), 
						('legs');
	"""

	result = executeQuery(insertQuery, [])
	if not result['success']:
		print("Failed to create table:", result)

def createExercises():
	# 1	biceps
	# 2	triceps
	# 3	shoulders
	# 4	chest
	# 5	back
	# 6	legs
	insertQuery = """INSERT INTO exercise (name, muscle_group_id)
					VALUES 
						('biceps curls', 1),
						('preacher curls', 1),
						('incline curls', 1),
						('rope hammer curls', 1),
						('wrist curls', 1),
						('21s', 1),

						('rope pulldown', 2),
						('overhead extension', 2),
						('skull crushers', 2),

						('barbell press', 3),
						('dumbbell press', 3),
						('lateral raise', 3),
						('front raise', 3),
						('rear delt fly', 3),
						('shrugs', 3),

						('bench press', 4),
						('incline dumbbell bench', 4),
						('decline press', 4),
						('machine flies', 4),

						('lat pulldown', 5),
						('back extension', 5),
						('seated rows', 5),
						('standing pulldown', 5),
						('supermans', 5),
						('pull ups', 5),

						('squat', 6),
						('leg extension', 6),
						('single leg curls', 6),
						('calf raises', 6),
						('lunges', 6),
						('side lunges', 6)




						;
	"""

	result = executeQuery(insertQuery, [])
	if not result['success']:
		print("Failed to create table:", result)


	return

if __name__ == "__main__":
	# createExerciseTable()
	# createMuscleGroups()
	# createMuscleGroupTable()
	# # createExercises()

	# createMuscleGroups()
	createExercises()