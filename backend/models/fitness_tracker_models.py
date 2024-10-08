from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from services.sql import sql_alchemy_utility

class MuscleGroup(sql_alchemy_utility.Base):
	__tablename__ = 'muscle_group_new'
	
	id = Column(Integer, primary_key=True)
	name = Column(String(50))

class Exercise(sql_alchemy_utility.Base):
	__tablename__ = 'exercise_new'
	
	id = Column(Integer, primary_key=True)
	name = Column(String(50))
	muscle_group_id = Column(Integer, ForeignKey('muscle_group.id'))

class WorkoutEntry(sql_alchemy_utility.Base):
	__tablename__ = 'workout_entries_new'
	
	id = Column(Integer, primary_key=True)
	workout_date = Column(String)  # Use appropriate type (e.g., Date)
	muscle_group_id = Column(Integer, ForeignKey('muscle_group.id'))
	exercise_id = Column(Integer, ForeignKey('exercise.id'))
	sets = Column(Integer)
	reps = Column(String)  # Assuming reps is stored as a string
	total_reps = Column(Integer)
	weight = Column(Integer)

	# Relationships
	muscle_group = relationship("MuscleGroup")
	exercise = relationship("Exercise")