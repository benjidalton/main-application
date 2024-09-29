standardPitchingColumns = {

	"W": {
		"columnName": "wins",
		"abbr": "W",
		"dataType": "INT(5)"
	},
	"L": {
		"columnName": "losses",
		"abbr": "L",
		"dataType": "INT(5)"
	},
	"win_loss_perc": {
		"columnName": "winLossPercent",
		"abbr": "winLossPerc",
		"dataType": "DECIMAL(5, 2)"
	},
	"earned_run_avg": {
		"columnName": "earnedRunAvg",
		"abbr": "ERA",
		"dataType": "DECIMAL(5, 2)"
	},
	"gamesPlayedPitcher": {
		"columnName": "gamesPlayedPitcher",
		"abbr": "GP",
		"dataType": "INT(10)"
	},
	"GS": {
		"columnName": "gamesStarted",
		"abbr": "GS",
		"dataType": "INT(10)"
	},
	"GF": {
		"columnName": "gamesFinished",
		"abbr": "GF",
		"dataType": "INT(10)"
	},
	"CG": {
		"columnName": "completeGames",
		"abbr": "CG",
		"dataType": "INT(10)"
	},
	"SHO": {
		"columnName": "shutouts",
		"abbr": "SO",
		"dataType": "INT(10)"
	},
	"SHO_team": {
		"columnName": "shutoutsOnTeam",
		"abbr": "SHOteam",
		"dataType": "INT(10)"
	},
	"SHO_cg": {
		"columnName": "shutoutsCGTeam",
		"abbr": "",
		"dataType": "INT(10)"
	},
	"SV": {
		"columnName": "saves",
		"abbr": "SV",
		"dataType": "INT(10)"
	},
	"IP": {
		"columnName": "inningsPitched",
		"abbr": "IP",
		"dataType": "INT(10)"
	},
	"HAllowed": {
		"columnName": "hitsAllowed",
		"abbr": "H",
		"dataType": "INT(10)"
	},
	"RAllowed": {
		"columnName": "runsAllowed",
		"abbr": "RA",
		"dataType": "INT(10)"
	},
	"ER": {
		"columnName": "earnedRuns",
		"abbr": "ER",
		"dataType": "INT(10)"
	},
	"HRAllowed": {
		"columnName": "homeRunsAllowed",
		"abbr": "HR",
		"dataType": "INT(10)"
	},
	"BBAllowed": {
		"columnName": "walksAllowed",
		"abbr": "BBA",
		"dataType": "INT(10)"
	},
	"IBBAllowed": {
		"columnName": "intentialWalksAllowed",
		"abbr": "IBBA",
		"dataType": "INT(10)"
	},
	"SOAllowed": {
		"columnName": "strikeoutsRecorded",
		"abbr": "SO",
		"dataType": "INT(10)"
	},
	"HBPAllowed": {
		"columnName": "hitBatters",
		"abbr": "HB",
		"dataType": "INT(10)"
	},
	"BK": {
		"columnName": "balks",
		"abbr": "BK",
		"dataType": "INT(10)"
	},
	"WP": {
		"columnName": "wildPitches",
		"abbr": "WP",
		"dataType": "INT(10)"
	},
	"batters_faced": {
		"columnName": "battersFaced",
		"abbr": "BF",
		"dataType": "INT(10)"
	},
	"earned_run_avg_plus": {
		"columnName": "adjustedEraPlus",
		"abbr": "aERA",
		"dataType": "INT(10)"
	},
	"fip": {
		"columnName": "fieldingIndPitching",
		"abbr": "FIP",
		"dataType": "DECIMAL(5, 2)"
	},
	"whip": {
		"columnName": "walksHitsPerNine",
		"abbr": "WHIP",
		"dataType": "DECIMAL(5, 2)"
	},
	"hits_per_nine": {
		"columnName": "hitsPerNine",
		"abbr": "HIP",
		"dataType": "DECIMAL(5, 2)"
	},
	"home_runs_per_nine": {
		"columnName": "homerunsPerNine",
		"abbr": "HRIP",
		"dataType": "DECIMAL(5, 2)"
	},
	"bases_on_balls_per_nine": {
		"columnName": "walksPerNine",
		"abbr": "BBIP",
		"dataType": "DECIMAL(5, 2)"
	},
	"strikeouts_per_nine": {
		"columnName": "strikeoutsPerNine",
		"abbr": "SOIP",
		"dataType": "DECIMAL(5, 2)"
	}, 
	"strikeouts_per_base_on_balls": {
		"columnName": "strikeoutsWalkRatio",
		"abbr": "kBBRatio",
		"dataType": "DECIMAL(5, 2)"
	},
	"pitchers_used": {
		"columnName": "pitchersUsed",
		"abbr": "",
		"dataType": "INT"
	},
	"age_pitch": {
		"columnName": "avgPitcherAge",
		"abbr": "agePitcher",
		"dataType": "decimal(5, 3)"
	},
	"runs_allowed_per_game": {
		"columnName": "runsAllowedPerGame",
		"abbr": "RAG",
		"dataType": "DECIMAL(5,3)"
	}
}

standardBattingColumns = {
    "G": {
        "columnName": "gamesPlayed",
        "abbr": "GP",
        "dataType": "INT(10)"
    },
    "PA": {
        "columnName": "plateAppearances",
        "abbr": "PA",
        "dataType": "INT(10)"
    },
    "AB": {
        "columnName": "atBats",
        "abbr": "AB",
        "dataType": "INT(10)"
    },
    "R": {
        "columnName": "runsScored",
        "abbr": "RS",
        "dataType": "INT(10)"
    },
    "H": {
        "columnName": "hits",
        "abbr": "H",
        "dataType": "INT(10)"
    },
    "2B": {
        "columnName": "doubles",
        "abbr": "2B",
        "dataType": "INT(10)"
    },
    "3B": {
        "columnName": "triples",
        "abbr": "3B",
        "dataType": "INT(10)"
    },
    "HR": {
        "columnName": "homeRuns",
        "abbr": "HR",
        "dataType": "INT(10)"
    },
    "RBI": {
        "columnName": "runsBattedIn",
        "abbr": "RBI",
        "dataType": "INT(10)"
    },
    "SB": {
        "columnName": "stolenBases",
        "abbr": "SB",
        "dataType": "INT(10)"
    },
    "CS": {
        "columnName": "caughtStealing",
        "abbr": "CS",
        "dataType": "INT(10)"
    },
    "BB": {
        "columnName": "walks",
        "abbr": "BB",
        "dataType": "INT(10)"
    },
    "SO": {
        "columnName": "strikeOuts",
        "abbr": "SO",
        "dataType": "INT(10)"
    },
    "batting_avg": {
        "columnName": "battingAverage",
        "abbr": "BA",
        "dataType": "DECIMAL(5, 2)"
    },
    "onbase_perc": {
        "columnName": "onBasePercentage",
        "abbr": "OBP",
        "dataType": "DECIMAL(5, 2)"
    },
    "slugging_perc": {
        "columnName": "sluggingPercentage",
        "abbr": "SLUG",
        "dataType": "DECIMAL(5, 2)"
    },
    "onbase_plus_slugging": {
        "columnName": "obpPlusSlugPercentage",
        "abbr": "OBPS",
        "dataType": "DECIMAL(5, 2)"
    },
    "onbase_plus_slugging_plus": {
        "columnName": "adjustedOpsPlus",
        "abbr": "aOBPS",
        "dataType": "DECIMAL(5, 2)"
    },
    "TB": {
        "columnName": "totalBases",
        "abbr": "TB",
        "dataType": "INT(10)"
    },
    "GIDP": {
        "columnName": "doublePlays",
        "abbr": "GIDP",
        "dataType": "INT(10)"
    },
    "HBP": {
        "columnName": "hitByPitch",
        "abbr": "HBP",
        "dataType": "INT(10)"
    },
    "SH": {
        "columnName": "sacrificeHits",
        "abbr": "SH",
        "dataType": "INT(10)"
    },
    "SF": {
        "columnName": "sacrificeFlies",
        "abbr": "SF",
        "dataType": "INT(10)"
    },
    "IBB": {
        "columnName": "intentialWalks",
        "abbr": "IBB",
        "dataType": "INT(10)"
    },
    "pos_season": {
        "columnName": "position",
        "abbr": "pos",
        "dataType": "VARCHAR(10)"
    },
	"LOB": {
		"columnName": "runnersLeftOnBase",
		"abbr": "LOB",
		"dataType": "INT"
	},
	"batters_used": {
		"columnName": "battersUsed",
		"abbr": "",
		"dataType": "INT"
	},
	"age_bat": {
		"columnName": "avgBatterAge",
		"abbr": "ageBat",
		"dataType": "decimal(5, 3)"
	},
	"runs_per_game": {
		"columnName": "runsPerGame",
		"abbr": "RG",
		"dataType": "DECIMAL(5,3)"
	}
}


# transformed_columns = {}

# for key, value in standardBattingColumns.items():
#     dataStatRef = value.pop('dataStatRef')
#     transformed_columns[dataStatRef] = value

# import json
# with open("transformed_columns.txt", "w") as file:
#     json.dump(transformed_columns, file, indent=4)

allColumns = standardBattingColumns | standardPitchingColumns

# columnDefinitions = []	
# for statName, details in standardPitchingColumns.items():
#     columnName = details['columnName']
#     dataType = details['dataType']
#     columnDefinitions.append(f"{columnName} {dataType}")

# # Iterate through batting columns
# for statName, details in standardBattingColumns.items():
#     columnName = details['columnName']
#     dataType = details['dataType']
#     columnDefinitions.append(f"{columnName} {dataType}")

# # Join the column definitions into a single string for the CREATE TABLE statement
# columnsString = ",\n".join(columnDefinitions)

# # Create the SQL CREATE TABLE query
# createQuery = f"""
# CREATE TABLE stats (
#     playerId INT PRIMARY KEY,
#     {columnsString}
# );
# """
# # Print the final SQL query
# print(createQuery)

# sqlUtility.executeQuery(createQuery, [])
