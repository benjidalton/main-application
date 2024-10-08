from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine, text, func
from sqlalchemy.orm import sessionmaker
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
load_dotenv()

#----- custom imports ------+
# from models.ExerciseTable import Exercise
from models.fitness_tracker_models import MuscleGroup, Exercise, WorkoutEntry
from services.sql import sql_alchemy_utility

APP_ACCESS_FITNESS_DB = os.getenv("APP_ACCESS_FITNESS_DB")
engine, Session = sql_alchemy_utility.create_db_session(APP_ACCESS_FITNESS_DB)

fitnessRoutes = Blueprint('fitnessRoutes', __name__, template_folder='templates')

#----- GET ROUTES ------+
@fitnessRoutes.route('/getExercisesByMuscleGroup', methods=['GET'])
def get_exercises_by_muscle_group():
	session = Session()
	try: 
		results = session.query(
			MuscleGroup.id.label('id'),
			MuscleGroup.name.label('muscleGroupName'),
			func.group_concat(Exercise.name, order_by=Exercise.id).label('exercises')
		).outerjoin(
			Exercise, Exercise.muscle_group_id == MuscleGroup.id
		).group_by(
			MuscleGroup.id
		).all()

		return [{'id': r.id, 'muscleGroupName': r.muscleGroupName, 'exercises': r.exercises} for r in results]
		
	except Exception as e:
		print(f"Error retrieving workouts: {e}")
		return []
	finally:
		session.close() 

@fitnessRoutes.route('/getWorkoutByDate', methods=['GET'])
def get_workout_by_date(workout_date):
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

@fitnessRoutes.route('/getWorkoutByDateRange', methods=['GET'])
def get_workout_by_date_range():
	minDate = request.args.get('minDate')
	maxDate = request.args.get('maxDate')

	session = Session()
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
			WorkoutEntry.workout_date.between(minDate, maxDate)
		).all()

		return [{'id': r.id, 'name': r.name, 'workoutDate': r.workoutDate,
				 'muscleGroupId': r.muscleGroupId, 'muscleGroup': r.muscleGroup,
				 'sets': r.sets, 'reps': r.reps, 'totalReps': r.totalReps,
				 'weight': r.weight} for r in results]

	except Exception as e:
		print(f"Error retrieving workouts: {e}")
		return [], 500  # Return an appropriate status code
	finally:
		session.close()  

#----- POST ROUTES -----+
@fitnessRoutes.route('/createNewExercise', methods=['POST'])
def create_new_exercise():
	session = Session()
	name = request.json['params']['name']
	muscleGroupId = request.json['params']['muscleGroupId']

	try: 
		new_exercise = Exercise(name=name, muscle_group_id=muscleGroupId)
		session.add(new_exercise) 
		session.commit()           
		print("Exercise inserted successfully!")
	
	except Exception as e:
		session.rollback() 
		print(f"Error inserting exercise: {e}")
	finally:
		session.close()

@fitnessRoutes.route('/createNewWorkout', methods=['POST'])
def create_new_workout():
	#----- exercise_data is instance of Exercise.js -----+
	workout_data = request.json['params']['workout'] 
	session = Session()  # Create a new session
	try:
		for exercise in workout_data:
			print('exercise in workout data: ', exercise)
			new_workout_entry = WorkoutEntry(
				workout_date=exercise['date'],
				muscle_group_id=exercise['muscleGroupId'],
				exercise_id=exercise['id'],
				sets=exercise['sets'],
				reps=','.join(map(str, exercise['reps'])), # Convert reps list to string
				total_reps=exercise['totalReps'],  
				weight=exercise['weight']
			)
			session.add(new_workout_entry)  # Add the new exercise to the session
			session.commit()            # Commit the transaction
		print("Exercise inserted successfully!")
	except Exception as e:
		session.rollback()          # Rollback in case of error
		print(f"Error inserting exercise: {e}")
	finally:
		session.close()

