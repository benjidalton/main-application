from openai import OpenAI
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from dotenv import load_dotenv
load_dotenv()
import sqlparse
from sql.sqlUtility import getDatabaseSchema, executeSelectQuery


client = OpenAI(api_key=os.getenv('OPEN_AI_SECRET_KEY'))
# Set up your OpenAI API key

def queryAgent(prompt: str):
	"""
		Sends a prompt to the AI model and retrieves the response.

		Args:
			prompt (str): * The input text that the AI model will respond to.

		Returns:
			str: The response message from the AI model, stripped of leading and trailing whitespace.
    """
	response = client.chat.completions.create(
		model="gpt-4o-mini",
		messages=[
			{"role": "system", "content": "You are a helpful assistant."},
			{
				"role": "user",
				"content": prompt
			}
		]
	)
	# return response.choices[0].text.strip()
	return response.choices[0].message

# Example schema prompt to send to the LLM
def createSchemaPrompt(schema: dict):
	"""
		Generates a descriptive prompt summarizing the tables and columns in the SQL database schema.

		Args:
			schema (dict): * A dictionary where keys are table names and values are lists of column names.

		Returns:
			str: A formatted string that lists all tables and their corresponding columns in the database schema.
    """
	prompt = "I have the following tables and columns in my SQL database:\n\n"
	for table, columns in schema.items():
		prompt += f"Table: {table}\nColumns: {', '.join(columns)}\n\n"

	return prompt

def provideContextForDbResponse(originalPrompt: str, dbResponse: str) -> str:
	"""
		Creates a contextual prompt for the AI model based on the original question and database response.

		Args:
			originalPrompt (str): * The user's original question.
			dbResponse (str): * The answer retrieved from the database.

		Returns:
			str: The AI-generated sentence that answers the original prompt using the database response.
    """
    
	context = f"I just asked you this:\n\n{originalPrompt}\n\n"
	answer = f"\nI checked my database and found this answer:\n\n{dbResponse}"
	prompt = context + answer + "\n\nCan you write a sentence answering the original prompt with the result from my database"
	return queryAgent(prompt).content

def getRawSqlQuery(response) -> str: 
	formmattedResponse = sqlparse.format(response.content, reindent=True, keyword_case='upper')
	return formmattedResponse.replace('```sql', '').replace('```', '').strip()

def getResponseFromDb(formattedSqlQuery):
	dbResponse = executeSelectQuery(formattedSqlQuery, [])

	print('db response: ', dbResponse)
	itemUrls = [{'name': item['name'], 'baseballReferenceUrl': item['baseballReferenceUrl']} for item in dbResponse['items']]

	formmattedDbResponse = ''
	for idx, item in enumerate(dbResponse['items']):
		for key, value in item.items():
			if key == 'baseballReferenceUrl':
				# skip the url so it doesnt display on front end
				continue
			formmattedDbResponse += f"{key}: {value}\n"
		formmattedDbResponse += "\n"

	return formmattedDbResponse, itemUrls




def createSqlQuery(userPrompt: str, promptType: str):
	"""
		Generates a MariaDB SQL query based on the user's prompt and the database schema.

		This function checks if the prompt type is a database query, retrieves the database schema,
		constructs a detailed prompt for query generation, and processes the response.

		Args:
			userPrompt (str): * The user's question or request for an SQL query.
			promptType (str): * The type of the prompt, expected to be 'DB Query'.

		Returns:
			tuple: A tuple containing:
				- toolTipString (str): A string with additional information if needed.
				- formattedSqlQuery (str or None): The generated SQL query or None if not applicable.
				- answerWithContext (str): Contextual information about the query result.
				- itemUrls (list or None): Any applicable URLs from the database.
    """
    
	if promptType != 'DB Query':
		print('you didnt  have db query chosen')
		return
	
	# load db schema
	dataBaseSchema = getDatabaseSchema()
	
	# unpack database schema dict to a string for use in full prompt to llm
	schemaPrompt = createSchemaPrompt(dataBaseSchema)

	moreInfoString = 'MORE INFORMATION NEEDED'
	fullPrompt = schemaPrompt + f"""\n\nHow would you write a MariaDB SQL query to answer this:\n
										{userPrompt}
									\nPlease don't return any context, just the query you would use. 
									It is imperative you provide any url references from the database applicable to the items in the response.
									\nDon't include qualifiers like 'player' or 'team' when defining values in the query. For example, if I ask you for the name
									of the team with the most home runs, just use the 'teams' table and the 'name' column. 
									\nMake sure to select the data that would help with answering the prompt so it can be used to provide more context.
									\n\n If you don't think you can answer the question with the database schema provided, provide information on what I can add to my 
										database schedma that would help you. Start your response with {moreInfoString} in all caps so I can handle it. """

	response = queryAgent(fullPrompt)

	if moreInfoString in response.content:
		print('more info needed for response')
		removedInfo = response.content.replace(f'{moreInfoString}', '').strip()
		toolTipString = removedInfo
		answerWithContext = removedInfo
		print('response with moreInfo removed', removedInfo)
		formattedSqlQuery = None
		itemUrls = None
		return toolTipString, formattedSqlQuery, answerWithContext, itemUrls

	toolTipString = getRawSqlQuery(response)

	formattedSqlQuery = f"{toolTipString}" 

	formmattedDbResponse, itemUrls = getResponseFromDb(formattedSqlQuery)

	answerWithContext = provideContextForDbResponse(userPrompt, formmattedDbResponse)
	return toolTipString, formattedSqlQuery, answerWithContext, itemUrls