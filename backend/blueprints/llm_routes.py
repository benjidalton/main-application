from flask import Blueprint, request
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from sql.sqlUtility import getDatabaseSchema, executeSelectQuery
# from services.llm.openAIAgent import createSqlQuery
# custom imports
from models.LLMAgent import llm_agent

import logging
_logger = logging.getLogger('app')

llm_routes = Blueprint('llm_routes', __name__, template_folder='templates')


@llm_routes.route('/fetchLLMResponse', methods=['GET'])
def fetch_llm_response():
	prompt = request.args.get('prompt')
	promptType = request.args.get('promptType')

	rawSqlQuery, formattedSqlQuery, dbResponse, itemUrls = llm_agent.create_sql_query(prompt, promptType)
	return [rawSqlQuery, formattedSqlQuery, dbResponse, itemUrls]