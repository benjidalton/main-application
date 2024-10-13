from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
#----- custom imports ------+
from services.sql.sql_alchemy_utility import Base 

class MuscleGroup(Base):
	__tablename__ = 'muscle_group'
	
	id = Column(Integer, primary_key=True)
	name = Column(String(50))

	def __init__(self, name):
		self.name = name


class Exercise(Base):
	__tablename__ = 'exercise'
	
	id = Column(Integer, primary_key=True)
	name = Column(String(50))
	default_weight = Column(Integer) 

	#----- relationship ------+
	muscle_group_id = Column(Integer, ForeignKey('muscle_group.id'))

	def __init__(self, name, muscle_group_id, default_weight = 0):
		self.name = name
		self.muscle_group_id = muscle_group_id
		self.default_weight = default_weight

class WorkoutEntry(Base):
	__tablename__ = 'workout_entries'
	
	id = Column(Integer, primary_key=True)
	workout_date = Column(String(50)) 
	muscle_group_id = Column(Integer, ForeignKey('muscle_group.id'))
	exercise_id = Column(Integer, ForeignKey('exercise.id'))
	sets = Column(Integer)
	reps = Column(String(50))
	total_reps = Column(Integer)
	weight = Column(Integer)
	weight_reps_aggregate = Column(Integer)

	#----- relationships ------+
	muscle_group = relationship("MuscleGroup")
	exercise = relationship("Exercise")

	def __init__(self, workout_date, muscle_group_id, exercise_id, sets, reps, total_reps, weight, weight_reps_aggregate ):
		self.workout_date = workout_date
		self.muscle_group_id = muscle_group_id
		self.exercise_id = exercise_id
		self.sets = sets
		self.reps = reps
		self.total_reps = total_reps
		self.weight = weight
		self.weight_reps_aggregate = weight_reps_aggregate 
