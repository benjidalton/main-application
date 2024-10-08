from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
load_dotenv()

# custom imports
import backend.services.sql.sql_utility as sql_utility
import services.sql.fitnessData as fitnessData
from models.ExerciseTable import Exercise
from models.fitness_tracker_models import MuscleGroup, Exercise, WorkoutEntry
from services.sql import sql_alchemy_utility



APP_ACCESS_FITNESS_DB = os.getenv("APP_ACCESS_FITNESS_DB")
engine, Session = sql_alchemy_utility.create_db_session(APP_ACCESS_FITNESS_DB)

fitnessRoutes = Blueprint('fitnessRoutes', __name__, template_folder='templates')


@fitnessRoutes.route('/getExercisesByMuscleGroup', methods=['GET'])
def getExercisesByMuscleGroup():
	query = fitnessData.GET_EXERCISES_BY_MUSCLE_GROUP
	params = []
	return sql_utility.executeQuery(APP_ACCESS_FITNESS_DB, query, params)

@fitnessRoutes.route('/insertNewExercise', methods=['GET'])
def insertNewExercise():
	name = request.args.get('name')
	muscleGroupId = request.args.get('muscleGroupId')
	params = [name, muscleGroupId]
	query = fitnessData.INSERT_NEW_EXERCISE
	return sql_utility.executeQuery(APP_ACCESS_FITNESS_DB, query, params)

@fitnessRoutes.route('/insertNewWorkout', methods=['POST'])
def insertNewWorkout():
	workoutData = request.json['params']['workout']
	responses = []  # To collect responses for each workout
	for workout in workoutData:
		try:
			# Extract values
			workoutDate = workout['date']
			muscleGroupId = workout['muscleGroupId']
			exerciseName = workout['name']
			sets = workout['sets']
			reps = ','.join(workout['reps'])  # Join the reps list into a comma-separated string
			weight = workout['weight']
			totalReps = workout.get('totalReps', 0)  # Default to 0 if not provided

			# Prepare SQL parameters
			params = [
				workoutDate,
				muscleGroupId,
				exerciseName,
				sets,
				reps,
				weight,
				totalReps
			]
			query = fitnessData.INSERT_NEW_WORKOUT
			
			# Execute the query
			sql_utility.executeQuery(APP_ACCESS_FITNESS_DB, query, params)
			responses.append({'status': 'success', 'exercise': exerciseName})  # Success message
		except Exception as e:
			responses.append({'status': 'error', 'exercise': exerciseName, 'message': str(e)})  # Error message

	return jsonify(responses)

@fitnessRoutes.route('/selectWorkoutByDate', methods=['GET'])
def selectWorkoutByDate():
	date = request.args.get('date')
	query = fitnessData.SELECT_WORKOUT_BY_DATE
	params = [date]
	return sql_utility.executeSelectQuery(APP_ACCESS_FITNESS_DB, query, params)

@fitnessRoutes.route('/selectWorkoutByDateRange', methods=['GET'])
def selectWorkoutByDateRange():
	minDate = request.args.get('minDate')
	maxDate = request.args.get('maxDate')
	query = fitnessData.SELECT_WORKOUT_BY_DATE_RANGE
	print('max date', maxDate)
	print('min date', minDate)
	print('query ', query)
	params = [minDate, maxDate]
	return sql_utility.executeSelectQuery(APP_ACCESS_FITNESS_DB, query, params)
