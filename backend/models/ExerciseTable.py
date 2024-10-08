from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Exercise(Base):
    __tablename__ = 'exercise'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    name = Column(String(50), nullable=False)
    muscleGroup = Column(String(50), nullable=False)
    sets = Column(Integer, nullable=False)
    reps = Column(String, nullable=False)  # Store as a comma-separated string
    weight = Column(Float, nullable=False)

    def __init__(self, date, name, muscleGroup, sets, reps, weight):
        self.date = date
        self.name = name
        self.muscleGroup = muscleGroup
        self.sets = sets
        self.reps = reps
        self.weight = weight