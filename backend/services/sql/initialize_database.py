from sqlalchemy import text
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from dotenv import load_dotenv
load_dotenv()
#----- custom imports ------+
from services.sql.sql_alchemy_utility import create_db_session, Base
from services.sql.sql_utility import execute_select_query 
from models.baseball_stats import Player, Team, PitchingPlayerStats, PitchingStats

from models.fitness_tracker import MuscleGroup, Exercise, WorkoutEntry

APP_ACCESS_FITNESS_DB = os.getenv("APP_ACCESS_FITNESS_DB")
APP_ACCESS_BASEBALL_DB = os.getenv("APP_ACCESS_BASEBALL_DB")

fitness_db_engine, fitness_db_session = create_db_session(APP_ACCESS_FITNESS_DB)
baseball_db_engine, baseball_db_session = create_db_session(APP_ACCESS_BASEBALL_DB)


def add_to_session(Session, items, table_name):
	session = Session()
	session.add_all(items)

	try:
		# Commit the session to save changes
		session.commit()
		print(f"{table_name} inserted successfully!")
	except Exception as e:
		session.rollback()  # Rollback in case of error
		print(f"An error occurred: {e}")
	finally:
		session.close()  

# Baseball database

def create_baseball_tables():
	with baseball_db_engine.connect() as connection:
		# Drop the table if it exists
		connection.execute(text("SET FOREIGN_KEY_CHECKS = 0")) # ignore foreign key checks when deleting tables

		connection.execute(text("DROP TABLE IF EXISTS players_new"))
		connection.execute(text("DROP TABLE IF EXISTS teams_new"))
		connection.execute(text("DROP TABLE IF EXISTS pitching_stats"))
		connection.execute(text("DROP TABLE IF EXISTS pitching_player_stats"))
		connection.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
		
		print("Tables dropped if they existed.")

		# Create the only the tables you want for this database
		# The Base object has all the tables in every database so you need to specific which tables when initalizing the db
		Base.metadata.create_all(baseball_db_engine, tables=[
		    Player.__table__,
		    Team.__table__,
		    PitchingStats.__table__,
		    PitchingPlayerStats.__table__
		])

		print("Tables created successfully!")

	import_teams_to_new_db()
	import_players_to_new_db()
	import_pitching_stats_to_new_db()

def initialize_pitching_stats_table():

	pitching_stats = [
		PitchingStats('wins'),
		PitchingStats('losses'),
		PitchingStats('win_loss_perc'),
		PitchingStats('earned_run_avg'),
		PitchingStats('games_started'),
		PitchingStats('games_finished'),
		PitchingStats('complete_games'),
		PitchingStats('shutouts'),
		PitchingStats('saves'),
		PitchingStats('innings_pitched'),
		PitchingStats('hits_allowed'),
		PitchingStats('runs_allowed'),
		PitchingStats('earned_runs'),
		PitchingStats('home_runs_allowed'),
		PitchingStats('walks_allowed'),
		PitchingStats('intentional_walks'),
		PitchingStats('strikeouts_recorded'),
		PitchingStats('hit_batters'),
		PitchingStats('balks'),
		PitchingStats('wild_pitches'),
		PitchingStats('batters_faced'),
		PitchingStats('adjusted_era_plus'),
		PitchingStats('fielding_ind_pitching'),
		PitchingStats('walks_hits_per_nine'),
		PitchingStats('hits_per_nine'),
		PitchingStats('homeruns_per_nine'),
		PitchingStats('walks_per_nine'),
		PitchingStats('strikeouts_per_nine'),
		PitchingStats('strikeout_walk_ratio')
	]

	add_to_session(baseball_db_session, pitching_stats, 'pitching_stats')

def import_players_to_new_db():
	select_query = """ select * from players """
	
	data = execute_select_query(APP_ACCESS_BASEBALL_DB, select_query, [])
	players = [Player(player['name'], player['teamId'], player['baseballReferenceUrl'], player['pitcher']) for player in data['items']]

	add_to_session(baseball_db_session, players, 'players_new')

def import_teams_to_new_db():
	select_query = """ select * from teams """
	
	data = execute_select_query(APP_ACCESS_BASEBALL_DB, select_query, [])
	teams = [Team(team['name'], team['league'], team['division'], team['baseballReferenceUrl'], team['logoName']) for team in data['items']]
	
	add_to_session(baseball_db_session, teams, 'teams_new')

def import_pitching_stats_to_new_db():
	select_query = """
		select
			playerId,
			wins,
			losses,
			winLossPercent,
			earnedRunAvg,
			gamesStarted,
			gamesFinished,
			completeGames,
			shutouts,
			saves,
			inningsPitched,
			hitsAllowed,
			runsAllowed,
			earnedRuns,
			homeRunsAllowed,
			walksAllowed,
			intentialWalksAllowed,
			strikeoutsRecorded,
			hitBatters,
			balks,
			wildPitches,
			battersFaced,
			adjustedEraPlus,
			fieldingIndPitching,
			walksHitsPerNine,
			hitsPerNine,
			homerunsPerNine,
			walksPerNine,
			strikeoutsPerNine,
			strikeoutsWalkRatio

		from playerstats
		JOIN players ON playerstats.playerId = players.id
		WHERE players.pitcher = 1;
	"""

	data = execute_select_query(APP_ACCESS_BASEBALL_DB, select_query, [])
	stats = []
	for stat in data['items']:
		stats.append(PitchingPlayerStats(
			player_id=stat['playerId'],
			wins=stat['wins'],
			losses=stat['losses'],
			win_loss_perc=stat['winLossPercent'],
			earned_run_avg=stat['earnedRunAvg'],
			games_started=stat['gamesStarted'],
			games_finished=stat['gamesFinished'],
			complete_games=stat['completeGames'],
			shutouts=stat['shutouts'],
			saves=stat['saves'],
			innings_pitched=stat['inningsPitched'],
			hits_allowed=stat['hitsAllowed'],
			runs_allowed=stat['runsAllowed'],
			earned_runs=stat['earnedRuns'],
			home_runs_allowed=stat['homeRunsAllowed'],
			walks_allowed=stat['walksAllowed'],
			intentional_walks=stat['intentialWalksAllowed'],  # Note the typo in 'intential'
			strikeouts_recorded=stat['strikeoutsRecorded'],
			hit_batters=stat['hitBatters'],
			balks=stat['balks'],
			wild_pitches=stat['wildPitches'],
			batters_faced=stat['battersFaced'],
			adjusted_era_plus=stat['adjustedEraPlus'],
			fielding_ind_pitching=stat['fieldingIndPitching'],
			walks_hits_per_nine=stat['walksHitsPerNine'],
			hits_per_nine=stat['hitsPerNine'],
			homeruns_per_nine=stat['homerunsPerNine'],
			walks_per_nine=stat['walksPerNine'],
			strikeouts_per_nine=stat['strikeoutsPerNine'],
			strikeout_walk_ratio=stat['strikeoutsWalkRatio']
		))

		add_to_session(baseball_db_session, stats, 'PitchingPlayerStats')


# Fitness database

def create_fitness_tables():
	with fitness_db_engine.connect() as connection:
		# Drop the table if it exists
		connection.execute(text("SET FOREIGN_KEY_CHECKS = 0")) # ignore foreign key checks when deleting tables

		connection.execute(text("DROP TABLE IF EXISTS exercise"))
		connection.execute(text("DROP TABLE IF EXISTS muscle_group"))
		connection.execute(text("DROP TABLE IF EXISTS workout_entries"))

		connection.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
		print("Tables dropped if they existed.")

		# Create the only the tables you want for this database
		# The Base object has all the tables in every database so you need to specific which tables when initalizing the db
		Base.metadata.create_all(fitness_db_engine, tables=[
		    MuscleGroup.__table__,
		    Exercise.__table__,
		    WorkoutEntry.__table__
		])
		print("Tables created successfully!")
	
	insert_muscle_groups()
	insert_exercises()

def insert_exercises():

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
	add_to_session(fitness_db_session, exercises, 'exercises')

def insert_muscle_groups():
	# Define muscle groups to insert
	muscle_groups = [
		MuscleGroup(name='Biceps'),
		MuscleGroup(name='Triceps'),
		MuscleGroup(name='Shoulders'),
		MuscleGroup(name='Chest'),
		MuscleGroup(name='Back'),
		MuscleGroup(name='Legs'),
	]

	add_to_session(fitness_db_session, muscle_groups, 'muscle_groups')


def main():
	create_fitness_tables()
	# create_baseball_tables()


if __name__ == "__main__":
	
	main()