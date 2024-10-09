from sqlalchemy import text
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from dotenv import load_dotenv
load_dotenv()
#----- custom imports ------+
from services.sql.sql_alchemy_utility import create_db_session, Base

from backend.models.fitness_tracker import MuscleGroup, Exercise, WorkoutEntry

APP_ACCESS_FITNESS_DB = os.getenv("APP_ACCESS_FITNESS_DB")
engine, Session = create_db_session(APP_ACCESS_FITNESS_DB)

# Create the table
def create_tables():

	with engine.connect() as connection:
		# Drop the table if it exists
		connection.execute(text("SET FOREIGN_KEY_CHECKS = 0"))

		# Drop the tables
		connection.execute(text("DROP TABLE IF EXISTS workout_entries_new"))
		connection.execute(text("DROP TABLE IF EXISTS exercise_new"))
		connection.execute(text("DROP TABLE IF EXISTS muscle_group_new"))

		# Re-enable foreign key checks
		connection.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
		print("Tables dropped if they existed.")

		# Create the tables
		print('sql alchemy base',  Base.metadata.tables.keys())
		print('\n\n\nengine:', engine)
		Base.metadata.create_all(engine)
		print("Tables created successfully!")


def insert_exercises():
	# Create a session
	session = Session()

	# Create a list of Exercise instances
	exercises = [
		Exercise(name='biceps curls', muscle_group_id=1),
		Exercise(name='preacher curls', muscle_group_id=1),
		Exercise(name='incline curls', muscle_group_id=1),
		Exercise(name='rope hammer curls', muscle_group_id=1),
		Exercise(name='wrist curls', muscle_group_id=1),
		Exercise(name='21s', muscle_group_id=1),

		Exercise(name='rope pulldown', muscle_group_id=2),
		Exercise(name='overhead extension', muscle_group_id=2),
		Exercise(name='skull crushers', muscle_group_id=2),

		Exercise(name='barbell press', muscle_group_id=3),
		Exercise(name='dumbbell press', muscle_group_id=3),
		Exercise(name='lateral raise', muscle_group_id=3),
		Exercise(name='front raise', muscle_group_id=3),
		Exercise(name='rear delt fly', muscle_group_id=3),
		Exercise(name='shrugs', muscle_group_id=3),

		Exercise(name='bench press', muscle_group_id=4),
		Exercise(name='incline dumbbell bench', muscle_group_id=4),
		Exercise(name='decline press', muscle_group_id=4),
		Exercise(name='machine flies', muscle_group_id=4),

		Exercise(name='lat pulldown', muscle_group_id=5),
		Exercise(name='back extension', muscle_group_id=5),
		Exercise(name='seated rows', muscle_group_id=5),
		Exercise(name='standing pulldown', muscle_group_id=5),
		Exercise(name='supermans', muscle_group_id=5),
		Exercise(name='pull ups', muscle_group_id=5),

		Exercise(name='squat', muscle_group_id=6),
		Exercise(name='leg extension', muscle_group_id=6),
		Exercise(name='single leg curls', muscle_group_id=6),
		Exercise(name='calf raises', muscle_group_id=6),
		Exercise(name='lunges', muscle_group_id=6),
		Exercise(name='side lunges', muscle_group_id=6),
	]

	# Add the exercises to the session
	session.add_all(exercises)

	try:
		# Commit the session to save changes
		session.commit()
		print("Exercises inserted successfully!")
	except Exception as e:
		session.rollback()  # Rollback in case of error
		print(f"An error occurred: {e}")
	finally:
		session.close()  

def insert_muscle_groups():
	session = Session()

	# Define muscle groups to insert
	muscle_groups = [
		MuscleGroup(name='Biceps'),
		MuscleGroup(name='Triceps'),
		MuscleGroup(name='Shoulders'),
		MuscleGroup(name='Chest'),
		MuscleGroup(name='Back'),
		MuscleGroup(name='Legs'),
	]

	session.add_all(muscle_groups)

	try:
		session.commit()
		print("Muscle groups inserted successfully!")
	except Exception as e:
		session.rollback()
		print(f"An error occurred: {e}")
	finally:
		session.close()

def main():
	 
	create_tables()
	insert_muscle_groups()
	insert_exercises()

if __name__ == "__main__":
	main()