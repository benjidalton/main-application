GET_TEAMS_DATA = """ SELECT id, name, league, division, logoName FROM teams """

GET_PLAYERS_DATA = """ 
					SELECT 
						players.id as id,
						players.name AS name, 
						players.baseballReferenceUrl as baseballReferenceUrl,
						teams.name AS teamName,
						teams.logoName as teamLogoName
					FROM 
						players
					JOIN teams ON 
					teams.id = players.teamId 
					
					"""

GET_TEAM_PLAYERS = """
					SELECT 
					    players.id AS id,
					    players.name AS name,
						players.baseballReferenceUrl as baseballReferenceUrl, 
					    teams.name AS teamName,
					    teams.logoName AS teamLogoName
					FROM 
					    players
					JOIN 
					    teams ON teams.id = players.teamId
					WHERE 
					    teams.id = %s;
					"""
