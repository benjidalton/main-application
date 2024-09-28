from flask import Blueprint
from flask import jsonify, request
import json

import sql.sqlUtility as sqlUtility
import sql.loadData as loadData

import logging
_logger = logging.getLogger('app')

routes = Blueprint('routes', __name__, template_folder='templates')

routeMapping = {
            "getTeamsData": loadData.GET_TEAMS_DATA,
			"getPlayersData": loadData.GET_PLAYERS_DATA,
			"getPlayersOnTeam": loadData.GET_TEAM_PLAYERS
		}

@routes.route('/getTeamsData', methods=['GET'])
def getTeamsData():
	params = []
	selectSql = loadData.GET_TEAMS_DATA
	return sqlUtility.executeSelectQuery(selectSql, params)

@routes.route('/getPlayersData', methods=['GET'])
def getPlayersData():
	params = []
	selectSql = loadData.GET_PLAYERS_DATA
	
	return sqlUtility.executeSelectQuery(selectSql, params)

@routes.route('/getPlayersOnTeam', methods=['GET'])
def getPlayersOnTeam():
	params = request.args.get('teamId')
	selectSql = loadData.GET_TEAM_PLAYERS
	return sqlUtility.executeSelectQuery(selectSql, params)