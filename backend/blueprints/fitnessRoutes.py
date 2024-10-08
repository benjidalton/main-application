from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
load_dotenv()

# custom imports
import services.sql.sqlUtility as sqlUtility
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
	return sqlUtility.executeQuery(APP_ACCESS_FITNESS_DB, query, params)

@fitnessRoutes.route('/insertNewExercise', methods=['GET'])
def insertNewExercise():
	name = request.args.get('name')
	muscleGroupId = request.args.get('muscleGroupId')
	params = [name, muscleGroupId]
	query = fitnessData.INSERT_NEW_EXERCISE
	return sqlUtility.executeQuery(APP_ACCESS_FITNESS_DB, query, params)

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
			sqlUtility.executeQuery(APP_ACCESS_FITNESS_DB, query, params)
			responses.append({'status': 'success', 'exercise': exerciseName})  # Success message
		except Exception as e:
			responses.append({'status': 'error', 'exercise': exerciseName, 'message': str(e)})  # Error message

	return jsonify(responses)

@fitnessRoutes.route('/insertNewWorkoutWithSessionMaker', methods=['POST'])
def insertNewWorkoutWithSessionMaker():
	exercise_data = request.json['params']['workout']
	responses = []  # To collect responses for each workout
	session = Session()  # Create a new session
	try:
		new_exercise = Exercise(
			date=exercise_data['date'],
			name=exercise_data['name'],
			muscleGroup=exercise_data['muscleGroup'],
			sets=exercise_data['sets'],
			reps=','.join(map(str, exercise_data['reps'])),  # Convert reps list to string
			weight=exercise_data['weight']
		)
		session.add(new_exercise)  # Add the new exercise to the session
		session.commit()            # Commit the transaction
		print("Exercise inserted successfully!")
	except Exception as e:
		session.rollback()          # Rollback in case of error
		print(f"Error inserting exercise: {e}")
	finally:
		session.close()

@fitnessRoutes.route('/selectWorkoutByDateWithSessionMaker', methods=['GET'])
def selectWorkoutByDateWithSessionMaker(workout_date):
	session = Session()  # Create a new session
	try:
		results = session.query(
			WorkoutEntry.id.label('id'),
			Exercise.name.label('name'),
			WorkoutEntry.workout_date.label('workoutDate'),
			WorkoutEntry.muscle_group_id.label('muscleGroupId'),
			MuscleGroup.name.label('muscleGroup'),
			WorkoutEntry.sets,
			WorkoutEntry.reps,
			WorkoutEntry.total_reps.label('totalReps'),
			WorkoutEntry.weight
		).join(
			MuscleGroup, WorkoutEntry.muscle_group_id == MuscleGroup.id
		).join(
			Exercise, WorkoutEntry.exercise_id == Exercise.id
		).filter(
			WorkoutEntry.workout_date == workout_date
		).all()

		return [{'id': r.id, 'name': r.name, 'workoutDate': r.workoutDate,
				 'muscleGroupId': r.muscleGroupId, 'muscleGroup': r.muscleGroup,
				 'sets': r.sets, 'reps': r.reps, 'totalReps': r.totalReps,
				 'weight': r.weight} for r in results]
		
	except Exception as e:
		print(f"Error retrieving workouts: {e}")
		return []
	finally:
		session.close() 


@fitnessRoutes.route('/selectWorkoutByDate', methods=['GET'])
def selectWorkoutByDate():
	date = request.args.get('date')
	query = fitnessData.SELECT_WORKOUT_BY_DATE
	params = [date]
	return sqlUtility.executeSelectQuery(APP_ACCESS_FITNESS_DB, query, params)

@fitnessRoutes.route('/selectWorkoutByDateRange', methods=['GET'])
def selectWorkoutByDateRange():
	minDate = request.args.get('minDate')
	maxDate = request.args.get('maxDate')
	query = fitnessData.SELECT_WORKOUT_BY_DATE_RANGE
	print('max date', maxDate)
	print('min date', minDate)
	print('query ', query)
	params = [minDate, maxDate]
	return sqlUtility.executeSelectQuery(APP_ACCESS_FITNESS_DB, query, params)

