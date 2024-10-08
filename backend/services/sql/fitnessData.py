
GET_EXERCISES_BY_MUSCLE_GROUP = """SELECT 
                                    mg.id as id,
                                    mg.name AS muscleGroup,
                               	 	GROUP_CONCAT(e.name ORDER BY e.id SEPARATOR ', ') AS exercises
                                FROM 
                                    muscle_group mg
                                LEFT JOIN 
                                    exercise e ON e.muscle_group_id = mg.id
                                GROUP BY 
                                    mg.id;"""

INSERT_NEW_EXERCISE = """INSERT INTO exercise (name, muscle_group_id)
		                    VALUES (%s, %s)
                        """

INSERT_NEW_WORKOUT =  """INSERT INTO workout_entries (workout_date, muscle_group_id, exercise_id, sets, reps, weight, total_reps) 
				            VALUES (
            					%s, 
            					%s, 
            					(SELECT id FROM exercise WHERE name = %s),
            					%s, 
            					%s, 
								%s, 
            					%s
            				)"""

SELECT_WORKOUT_BY_DATE = """SELECT 
							    we.exercise_id as id,
								e.name AS name, 
								we.workout_date AS workoutDate,      
								we.muscle_group_id as muscleGroupId,         
							    mg.name AS muscleGroup,  
								we.sets,
								we.reps,
								we.total_reps as totalReps,
								we.weight   
							FROM 
							    workout_entries we
							JOIN 
							    muscle_group mg ON we.muscle_group_id = mg.id  
							JOIN 
							    exercise e ON we.exercise_id = e.id           
							WHERE 
							    we.workout_date = %s
							"""

SELECT_WORKOUT_BY_DATE_RANGE = """SELECT 
							    we.exercise_id as id,
								e.name AS name, 
								we.workout_date AS workoutDate,      
								we.muscle_group_id as muscleGroupId,         
							    mg.name AS muscleGroup,  
								we.sets,
								we.reps,
								we.total_reps as totalReps,
								we.weight   
							FROM 
							    workout_entries we
							JOIN 
							    muscle_group mg ON we.muscle_group_id = mg.id  
							JOIN 
							    exercise e ON we.exercise_id = e.id           
							WHERE 
							    we.workout_date BETWEEN %s AND %s;

							"""