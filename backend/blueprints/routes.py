from flask import Blueprint
from flask import jsonify, request
import json

import sql.sql_utility as sql_utility
import utility as util
import sql.loadData as loadData

import logging
_logger = logging.getLogger('app')

routes = Blueprint('routes', __name__, template_folder='templates')

routeMapping = {
            "getTeamsData": loadData.GET_TEAM_DATA,
		}

@routes.route('/getTeamsData', methods=['GET'])
#@jwt_required
def getTeamsData():
	selectSql = loadData.GET_TEAM_DATA
	return sql_utility.executeSelectSql((), selectSql)