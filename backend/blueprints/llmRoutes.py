from flask import Blueprint, request
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from sql.sqlUtility import getDatabaseSchema, executeSelectQuery
from services.llm.openAIAgent import createSqlQuery
import sqlparse

import logging
_logger = logging.getLogger('app')

llmRoutes = Blueprint('llmRoutes', __name__, template_folder='templates')


@llmRoutes.route('/fetchLLMResponse', methods=['GET'])
def fetchLLMResponse():
	prompt = request.args.get('prompt')
	promptType = request.args.get('promptType')

	rawSqlQuery, formattedSqlQuery, dbResponse, itemUrls = createSqlQuery(prompt, promptType)
	return [rawSqlQuery, formattedSqlQuery, dbResponse, itemUrls]