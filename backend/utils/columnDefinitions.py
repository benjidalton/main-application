
# keys for each obj is used to match with the 'data-stat' for the elements being web-scraped
# useful for matching data with columns for database entry
standardPitchingColumns = {

	"W": {
		"columnName": "wins",
		"dataType": "INT(5)"
	},
	"L": {
		"columnName": "losses",
		"dataType": "INT(5)"
	},
	"win_loss_perc": {
		"columnName": "winLossPercent",
		"dataType": "DECIMAL(5, 2)"
	},
	"earned_run_avg": {
		"columnName": "earnedRunAvg",
		"dataType": "DECIMAL(5, 2)"
	},
	"gamesPlayedPitcher": {
		"columnName": "gamesPlayedPitcher",
		"dataType": "INT(10)"
	},
	"GS": {
		"columnName": "gamesStarted",
		"dataType": "INT(10)"
	},
	"GF": {
		"columnName": "gamesFinished",
		"dataType": "INT(10)"
	},
	"CG": {
		"columnName": "completeGames",
		"dataType": "INT(10)"
	},
	"SHO": {
		"columnName": "shutouts",
		"dataType": "INT(10)"
	},
	"SHO_team": {
		"columnName": "shutoutsOnTeam",
		"dataType": "INT(10)"
	},
	"SHO_cg": {
		"columnName": "shutoutsCGTeam",
		"dataType": "INT(10)"
	},
	"SV": {
		"columnName": "saves",
		"dataType": "INT(10)"
	},
	"IP": {
		"columnName": "inningsPitched",
		"dataType": "INT(10)"
	},
	"HAllowed": {
		"columnName": "hitsAllowed",
		"dataType": "INT(10)"
	},
	"RAllowed": {
		"columnName": "runsAllowed",
		"dataType": "INT(10)"
	},
	"ER": {
		"columnName": "earnedRuns",
		"dataType": "INT(10)"
	},
	"HRAllowed": {
		"columnName": "homeRunsAllowed",
		"dataType": "INT(10)"
	},
	"BBAllowed": {
		"columnName": "walksAllowed",
		"dataType": "INT(10)"
	},
	"IBBAllowed": {
		"columnName": "intentionalWalksAllowed",
		"dataType": "INT(10)"
	},
	"SOAllowed": {
		"columnName": "strikeoutsRecorded",
		"dataType": "INT(10)"
	},
	"HBPAllowed": {
		"columnName": "hitBatters",
		"dataType": "INT(10)"
	},
	"BK": {
		"columnName": "balks",
		"dataType": "INT(10)"
	},
	"WP": {
		"columnName": "wildPitches",
		"dataType": "INT(10)"
	},
	"batters_faced": {
		"columnName": "battersFaced",
		"dataType": "INT(10)"
	},
	"earned_run_avg_plus": {
		"columnName": "adjustedEraPlus",
		"dataType": "INT(10)"
	},
	"fip": {
		"columnName": "fieldingIndPitching",
		"dataType": "DECIMAL(5, 2)"
	},
	"whip": {
		"columnName": "walksHitsPerNine",
		"dataType": "DECIMAL(5, 2)"
	},
	"hits_per_nine": {
		"columnName": "hitsPerNine",
		"dataType": "DECIMAL(5, 2)"
	},
	"home_runs_per_nine": {
		"columnName": "homerunsPerNine",
		"dataType": "DECIMAL(5, 2)"
	},
	"bases_on_balls_per_nine": {
		"columnName": "walksPerNine",
		"dataType": "DECIMAL(5, 2)"
	},
	"strikeouts_per_nine": {
		"columnName": "strikeoutsPerNine",
		"dataType": "DECIMAL(5, 2)"
	}, 
	"strikeouts_per_base_on_balls": {
		"columnName": "strikeoutsWalkRatio",
		"dataType": "DECIMAL(5, 2)"
	},
	"pitchers_used": {
		"columnName": "pitchersUsed",
		"dataType": "INT"
	},
	"age_pitch": {
		"columnName": "avgPitcherAge",
		"dataType": "decimal(5, 3)"
	},
	"runs_allowed_per_game": {
		"columnName": "runsAllowedPerGame",
		"dataType": "DECIMAL(5,3)"
	}
}

standardBattingColumns = {
	"G": {
		"columnName": "gamesPlayed",
		"dataType": "INT(10)"
	},
	"PA": {
		"columnName": "plateAppearances",
		"dataType": "INT(10)"
	},
	"AB": {
		"columnName": "atBats",
		"dataType": "INT(10)"
	},
	"R": {
		"columnName": "runsScored",
		"dataType": "INT(10)"
	},
	"H": {
		"columnName": "hits",
		"dataType": "INT(10)"
	},
	"2B": {
		"columnName": "doubles",
		"dataType": "INT(10)"
	},
	"3B": {
		"columnName": "triples",
		"dataType": "INT(10)"
	},
	"HR": {
		"columnName": "homeRuns",
		"dataType": "INT(10)"
	},
	"RBI": {
		"columnName": "runsBattedIn",
		"dataType": "INT(10)"
	},
	"SB": {
		"columnName": "stolenBases",
		"dataType": "INT(10)"
	},
	"CS": {
		"columnName": "caughtStealing",
		"dataType": "INT(10)"
	},
	"BB": {
		"columnName": "walks",
		"dataType": "INT(10)"
	},
	"SO": {
		"columnName": "strikeOuts",
		"dataType": "INT(10)"
	},
	"batting_avg": {
		"columnName": "battingAverage",
		"dataType": "DECIMAL(5, 2)"
	},
	"onbase_perc": {
		"columnName": "onBasePercentage",
		"dataType": "DECIMAL(5, 2)"
	},
	"slugging_perc": {
		"columnName": "sluggingPercentage",
		"dataType": "DECIMAL(5, 2)"
	},
	"onbase_plus_slugging": {
		"columnName": "obpPlusSlugPercentage",
		"dataType": "DECIMAL(5, 2)"
	},
	"onbase_plus_slugging_plus": {
		"columnName": "adjustedOpsPlus",
		"dataType": "DECIMAL(5, 2)"
	},
	"TB": {
		"columnName": "totalBases",
		"dataType": "INT(10)"
	},
	"GIDP": {
		"columnName": "doublePlays",
		"dataType": "INT(10)"
	},
	"HBP": {
		"columnName": "hitByPitch",
		"dataType": "INT(10)"
	},
	"SH": {
		"columnName": "sacrificeHits",
		"dataType": "INT(10)"
	},
	"SF": {
		"columnName": "sacrificeFlies",
		"dataType": "INT(10)"
	},
	"IBB": {
		"columnName": "intentonialWalks",
		"dataType": "INT(10)"
	},
	"pos_season": {
		"columnName": "position",
		"dataType": "VARCHAR(10)"
	},
	"LOB": {
		"columnName": "runnersLeftOnBase",
		"dataType": "INT"
	},
	"batters_used": {
		"columnName": "battersUsed",
		"dataType": "INT"
	},
	"age_bat": {
		"columnName": "avgBatterAge",
		"dataType": "decimal(5, 3)"
	},
	"runs_per_game": {
		"columnName": "runsPerGame",
		"dataType": "DECIMAL(5,3)"
	}
}

teamScheduleColumns = {
	"team_game": {
		"columnName": "gameNumber",
		"dataType": "INT(10)"
	},
	"date_game": {
		"columnName": "gameDate",
		"dataType": "DATE"
	},
	"homeORvis": {
		"columnName": "homeOrAway",
		"dataType": "DATE"
	},
	"opp_ID": {
		"columnName": "opponentId",
		"dataType": "INT(5)"
	},
    "win_loss_result": {
		"columnName": "winLoss",
		"dataType": "TEXT(1)"
	},
    "R": {
		"columnName": "runsScored",
		"dataType": "INT(5)"
	},
    "RA": {
		"columnName": "runsAllowed",
		"dataType": "INT(5)"
	},
    "extra_innings": {
		"columnName": "inningsReq",
		"dataType": "INT(5)"
	},
    "rank": {
		"columnName": "rank",
		"dataType": "INT(5)"
	},
    "games_back": {
		"columnName": "gamesBack",
		"dataType": "DECIMAL(5, 2)"
	},
    "opp_ID": {
		"columnName": "opponentId",
		"dataType": "INT(5)"
	},
    "winning_pitcher": {
		"columnName": "winningPitcherId",
		"dataType": "INT(5)"
	},
    "losing_pitcher": {
		"columnName": "losingPitcherId",
		"dataType": "INT(5)"
	},
    "saving_pitcher": {
		"columnName": "savingPitcherId",
		"dataType": "INT(5)"
	},
    "opp_ID": {
		"columnName": "opponentId",
		"dataType": "INT(5)"
	},
    "day_or_night": {
		"columnName": "dayOrNight",
		"dataType": "TEXT(1)"
	},
    "attendance": {
		"columnName": "attendance",
		"dataType": "INT(10)"
	},
    "opp_ID": {
		"columnName": "opponentId",
		"dataType": "INT(5)"
	},
}


allColumns = standardBattingColumns | standardPitchingColumns
