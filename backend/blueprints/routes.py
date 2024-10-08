from flask import Blueprint
from flask import jsonify, request
import json

import backend.services.sql.sql_utility as sql_utility
import backend.services.sql.baseball_queries as baseball_queries

import logging
_logger = logging.getLogger('app')

routes = Blueprint('routes', __name__, template_folder='templates')

routeMapping = {
            "getTeamsData": baseball_queries.GET_TEAMS_DATA,
			"getPlayersData": baseball_queries.GET_PLAYERS_DATA,
			"getPlayersOnTeam": baseball_queries.GET_TEAM_PLAYERS,
			"getAllTeamsPitchingStats": baseball_queries.GET_ALL_TEAMS_PITCHING_STATS
		}

@routes.route('/getTeamsData', methods=['GET'])
def get_teams_data():
	params = []
	selectSql = baseball_queries.GET_TEAMS_DATA
	return sql_utility.executeSelectQuery(selectSql, params)

@routes.route('/getPlayersData', methods=['GET'])
def get_players_data():
	params = []
	selectSql = baseball_queries.GET_PLAYERS_DATA
	
	return sql_utility.executeSelectQuery(selectSql, params)

@routes.route('/getPlayersOnTeam', methods=['GET'])
def get_players_on_team():
	params = request.args.get('teamId')
	selectSql = baseball_queries.GET_TEAM_PLAYERS
	return sql_utility.executeSelectQuery(selectSql, params)

@routes.route('/getAllTeamsPitchingStats', methods=['GET'])
def get_all_teams_pitching_stats():
	params = []
	selectSql = baseball_queries.GET_ALL_TEAMS_PITCHING_STATS
	return sql_utility.executeSelectQuery(selectSql, params)