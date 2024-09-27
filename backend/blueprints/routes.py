from flask import Blueprint
from flask import jsonify, request
import json

import sql.sql_utility as sql_utility
import utility as util
import sql.loadData as loadData

import logging
_logger = logging.getLogger('app')



routes = Blueprint('routes', __name__, template_folder='templates')
print('routes: ', routes)
routeMapping = {
            "getTeamNames": loadData.GET_TEAM_NAMES,
		}

@routes.route('/getTeamNames', methods=['GET'])
#@jwt_required
def getTeamNames():
	selectSql = loadData.GET_TEAM_NAMES

	
	return sql_utility.executeSelectSql((), selectSql)