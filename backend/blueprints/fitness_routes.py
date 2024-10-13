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
from models.fitness_tracker import MuscleGroup, Exercise, WorkoutEntry
from services.sql import sql_alchemy_utility

APP_ACCESS_FITNESS_DB = os.getenv("APP_ACCESS_FITNESS_DB")
engine, Session = sql_alchemy_utility.create_db_session(APP_ACCESS_FITNESS_DB)

fitness_routes = Blueprint('fitness_routes', __name__, template_folder='templates')

#----- GET ROUTES ------+
@fitness_routes.route('/getExercisesByMuscleGroup', methods=['GET'])
def get_exercises_by_muscle_group():
	session = Session()
	try: 
		results = session.query(
			MuscleGroup.id.label('id'),
			MuscleGroup.name.label('muscleGroupName'),
			func.group_concat(Exercise.id).label('exerciseIds'),
			func.group_concat(Exercise.name).label('exerciseNames'),
			func.group_concat(Exercise.default_weight).label('defaultWeights')
		).join(
			Exercise, Exercise.muscle_group_id == MuscleGroup.id
		).group_by(
			MuscleGroup.id
		).order_by(
			MuscleGroup.id  # or any other ordering you prefer
		).all()

		return [{'id': r.id, 'muscleGroupName': r.muscleGroupName, 'exerciseIds': r.exerciseIds, 'exerciseNames': r.exerciseNames, 'defaultWeights': r.defaultWeights} for r in results]
		
	except Exception as e:
		print(f"Error retrieving workouts: {e}")
		return []
	finally:
		session.close() 

@fitness_routes.route('/getWorkoutByDate', methods=['GET'])
def get_workout_by_date():
	workout_date = request.args.get('date')
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

@fitness_routes.route('/getWorkoutByDateRange', methods=['GET'])
def get_workout_by_date_range():
	minDate = request.args.get('minDate')
	maxDate = request.args.get('maxDate')

	session = Session()
	print('min date', minDate, "max date", maxDate)
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
		print('r', results)
		return [{'id': r.id, 'name': r.name, 'workoutDate': r.workoutDate,
				 'muscleGroupId': r.muscleGroupId, 'muscleGroup': r.muscleGroup,
				 'sets': r.sets, 'reps': r.reps, 'totalReps': r.totalReps,
				 'weight': r.weight} for r in results]

	except Exception as e:
		print(f"Error retrieving workouts: {e}")
		return [], 500  # Return an appropriate status code
	finally:
		session.close()  

@fitness_routes.route('/getWorkouts', methods=['GET'])
def get_workouts():
	muscle_groups = request.args.get('muscleGroups')
	exercises = request.args.get('exercises')
	dates = request.args.get('dates')

	session = Session()
	try:
		query = session.query(
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
		).group_by(
			WorkoutEntry.workout_date,
			Exercise.name,
			MuscleGroup.name  # Include other non-aggregated fields in the group_by
		)
		
		# handle if any muscle groups were defined in search params
		if muscle_groups is not None:
			muscle_group_list = [group.strip().lower() for group in muscle_groups.split(',')]
			query = query.filter(
				func.lower(MuscleGroup.name).in_(muscle_group_list)
			)

		# handle if any exercises were defined in search params
		if exercises is not None:
			exercises_list = [exercise.strip().lower() for exercise in exercises.split(',')]
			query = query.filter(
				func.lower(Exercise.name).in_(exercises_list)
			)
		
		# handle if any dates were defined in search params
		if dates is not None:
			dates_list = [dates.strip().lower() for dates in dates.split(',')]
			query = query.filter(
				WorkoutEntry.workout_date.in_(dates_list)
			)

		results = query.all()

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
@fitness_routes.route('/createNewExercise', methods=['POST'])
def create_new_exercise():
	session = Session()
	name = request.json['params']['name']
	muscle_group_id = request.json['params']['muscleGroupId']
	
	try: 
		new_exercise = Exercise(name=name, muscle_group_id=muscle_group_id)
		session.add(new_exercise) 
		session.commit()           
		return jsonify({"message": "Exercise inserted successfully!"}), 201

	except Exception as e:
		session.rollback() 
		# Return an error response
		return jsonify({"error": str(e)}), 400

	finally:
		session.close()

@fitness_routes.route('/createNewWorkout', methods=['POST'])
def create_new_workout():
	#----- workout_data is instance of Exercise.js -----+
	workout_data = request.json['params']['workout'] 
	session = Session()  

	try:
		for exercise in workout_data:
			exercise_record = session.query(Exercise).filter_by(name=exercise['name']).first()

			if not exercise_record:
				# if the exercise doesnt exist, add it to db
				# commit session and requiry to get the new id of the created exercise
				new_exercise = Exercise(name=exercise['name'], muscle_group_id=exercise['muscleGroupId'])
				session.add(new_exercise) 
				session.commit()  
				exercise_record = session.query(Exercise).filter_by(name=exercise['name']).first()
				


			weight = exercise['weight']
			total_reps = exercise['totalReps']
			if (total_reps == 0):
				# skip exercises where no reps performed 
				continue

			# Set default weight of exercise in db to weight entered
			# Used to auto fill the weight for that exercise next time it's chosen
			exercise_record.default_weight = weight

			# If the exercise exists, use its ID
			exercise_id = exercise_record.id if exercise_record else 'na'

			new_workout_entry = WorkoutEntry(
				workout_date=exercise['date'],
				muscle_group_id=exercise['muscleGroupId'],
				exercise_id=exercise_id,
				sets=exercise['sets'],
				reps=','.join(map(str, exercise['reps'])), # Convert reps list to string
				total_reps=exercise['totalReps'],  
				weight=exercise['weight'],
				weight_reps_aggregate=(int(weight) * int(total_reps))
			)
			session.add(new_workout_entry)

			session.commit()           
		return jsonify({"message": "Exercise(s) inserted successfully!"}), 201
	
	except Exception as e:
		session.rollback()          # Rollback in case of error
		return jsonify({"error": str(e)}), 400
	finally:
		session.close()

