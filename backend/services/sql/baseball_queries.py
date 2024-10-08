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

GET_ALL_TEAMS_PITCHING_STATS = """
								SELECT 
									teamstats.teamId as id,
								    teams.name as name, 
								    teams.league as league,
								    teams.division  as division,
								    teams.logoName as logoName,
								    teams.baseballReferenceUrl as baseballReferenceUrl, 
								    teamstats.pitchersUsed,
								    teamstats.avgPitcherAge,
								    teamstats.runsAllowedPerGame,
								    teamstats.wins,
								    teamstats.losses,
								    teamstats.winLossPercent,
								    teamstats.earnedRunAvg,
								    teamstats.gamesStarted,
								    teamstats.gamesFinished,
								    teamstats.completeGames,
								    teamstats.shutoutsOnTeam,
								    teamstats.shutoutsCGTeam,
								    teamstats.saves,
								    teamstats.inningsPitched,
								    teamstats.hitsAllowed,
								    teamstats.runsAllowed,
								    teamstats.earnedRuns,
								    teamstats.homeRunsAllowed,
								    teamstats.walksAllowed,
								    teamstats.intentionalWalksAllowed,
								    teamstats.strikeoutsRecorded,
								    teamstats.hitBatters,
								    teamstats.balks,
								    teamstats.wildPitches,
								    teamstats.battersFaced,
								    teamstats.adjustedEraPlus,
								    teamstats.fieldingIndPitching,
								    teamstats.walksHitsPerNine,
								    teamstats.hitsPerNine,
								    teamstats.homerunsPerNine,
								    teamstats.walksPerNine,
								    teamstats.strikeoutsPerNine,
								    teamstats.strikeoutsWalkRatio
								FROM 
								    teamstats
								JOIN 
								    teams ON teams.id = teamstats.teamId;
								""" 