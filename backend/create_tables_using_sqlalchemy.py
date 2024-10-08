from sqlalchemy import text
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from dotenv import load_dotenv
load_dotenv()
#----- custom imports ------+
from services.sql import sql_alchemy_utility

APP_ACCESS_FITNESS_DB = os.getenv("APP_ACCESS_FITNESS_DB")
engine, Session = sql_alchemy_utility.create_db_session(APP_ACCESS_FITNESS_DB)

# Create the table
def create_tables():
	with engine.connect() as connection:
		# Drop the table if it exists
		connection.execute(text("DROP TABLE IF EXISTS exercise_new"))
		connection.execute(text("DROP TABLE IF EXISTS muscle_group_new"))
		connection.execute(text("DROP TABLE IF EXISTS workout_entries_new"))
		print("Tables dropped if they existed.")

		# Create the tables
		sql_alchemy_utility.Base.metadata.create_all(engine)
		print("Tables created successfully!")

if __name__ == '__main__':
	create_tables()