from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
Base = declarative_base()
# from models.fitness_tracker import MuscleGroup, Exercise, WorkoutEntry
from dotenv import load_dotenv
load_dotenv()

APP_ACCESS_FITNESS_DB = os.getenv("APP_ACCESS_FITNESS_DB")
APP_ACCESS_BASESBALL_DB = os.getenv("APP_ACCESS_BASEBALL_DB")

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

def get_database_schema(db_name):
    # Create the database session
    print('db name', db_name)
    schemas = []
    for db_name in [APP_ACCESS_FITNESS_DB, APP_ACCESS_BASESBALL_DB]:


        engine, Session = create_db_session(db_name)

        # Create a MetaData instance
        metadata = MetaData()

        # Reflect the tables from the database
        metadata.reflect(bind=engine)

        # Print the table names and columns
        schema = {}
        for table in metadata.sorted_tables:
            schema[table.name] = [column.name for column in table.columns]
        schemas.append(schema)
       
    print('db_schemas', schemas)
          

    return schema


# if __name__ == "__main__":
#     schema = get_database_schema(APP_ACCESS_FITNESS_DB)
#     print('db schema: ', schema)
# Assuming you have already set up your environment and loaded your .env file
