from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
Base = declarative_base()
# from models.fitness_tracker import MuscleGroup, Exercise, WorkoutEntry
from dotenv import load_dotenv
load_dotenv()

APP_ACCESS_FITNESS_DB = os.getenv("APP_ACCESS_FITNESS_DB")

def create_db_session(db_name):
    db_user = os.getenv("APP_ACCESS_DB_USERNAME")
    db_pass = os.getenv("APP_ACCESS_DB_PASSWORD")
    db_host = os.getenv("APP_ACCESS_DB_HOSTNAME")
    db_port = os.getenv("APP_ACCESS_DB_PORT")

    # Construct the database URL
    DATABASE_URI = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    # Create an engine
    engine = create_engine(DATABASE_URI)

    # Create a session factory
    Session = sessionmaker(bind=engine)

    return engine, Session

# Assuming you have already set up your environment and loaded your .env file
