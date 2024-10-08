from openai import OpenAI
import json
import os
import sys
import sqlparse
from dotenv import load_dotenv
load_dotenv()
# custom imports
import backend.services.sql.sql_utility as sql_utility

class LLMAgent:
	def __init__(self, apiKey: str):
		self.client = OpenAI(api_key=apiKey)

	def queryAgent(self, prompt: str):
		"""
			Sends a prompt to the AI model and retrieves the response.

			Args:
				prompt (str): * The input text that the AI model will respond to.

			Returns:
				str: The response message from the AI model, stripped of leading and trailing whitespace.
		"""
		response = self.client.chat.completions.create(
			model="gpt-4o-mini",
			messages=[
				{"role": "system", "content": "You are a helpful assistant."},
				{
					"role": "user",
					"content": prompt
				}
			]
		)

		print('response in queryAgent to check the typing of the response: ', response.choices[0].message)

		return response.choices[0].message
	

	def createSchemaPrompt(self, schema: dict) -> str:
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

	def provideContextForDbResponse(self, originalPrompt: str, dbResponse: str) -> str:
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
		prompt = context + answer + "\n\nCan you write a sentence answering the original prompt with the result from my database?"
		return self.queryAgent(prompt).content

	def getRawSqlQuery(self, response) -> str:
		"""Formats and cleans the SQL response from the AI model."""
		formatted_response = sqlparse.format(response.content, reindent=True, keyword_case='upper')
		return formatted_response.replace('```sql', '').replace('```', '').strip()

	def getResponseFromDb(self, formattedSqlQuery) -> tuple:
		"""Executes the SQL query and retrieves the response from the database."""
		dbResponse = sql_utility.executeSelectQuery(formattedSqlQuery, [])
		print('db response: ', dbResponse)
		# Get the baseball reference url and name for each item returned
		# Used to create href links on the front end
		 
		itemUrls = [
			{'name': item['name'], 'baseballReferenceUrl': item['baseballReferenceUrl']} 
			if 'baseballReferenceUrl' in item 
			else None
			for item in dbResponse['items'] 
		] 
		
		formattedDbResponse = ''
		for item in dbResponse['items']:
			for key, value in item.items():
				if key == 'baseballReferenceUrl':
					# Skip the baseball reference url so that it doesn't get included in the actual string displayed on front end
					continue
				formattedDbResponse += f"{key}: {value}\n"
			formattedDbResponse += "\n"

		return formattedDbResponse, itemUrls

	def createSqlQuery(self, userPrompt: str, promptType: str) -> tuple:
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
			print('You did not have DB Query chosen')
			return

		# Load database schema
		databaseSchema = sql_utility.getDatabaseSchema()
		schemaPrompt = self.createSchemaPrompt(databaseSchema)

		moreInfoString = 'MORE INFORMATION NEEDED'
		full_prompt = schemaPrompt + f"""\n\nHow would you write a MariaDB SQL query to answer this:\n
										{userPrompt}
									\nPlease don't return any context, just the query you would use. 
									It is imperative you provide any URL references from the database applicable to the items in the response.
									\nDon't include qualifiers like 'player' or 'team' when defining values in the query. For example, if I ask you for the name
									of the team with the most home runs, just use the 'teams' table and the 'name' column. 
									\nMake sure to select the data that would help with answering the prompt so it can be used to provide more context.
									\n\n If you don't think you can answer the question with the database schema provided, provide information on what I can add to my 
										database schema that would help you. Start your response with {moreInfoString} in all caps so I can handle it. """

		response = self.queryAgent(full_prompt)

		if moreInfoString in response.content:
			print('More info needed for response')
			removedInfo = response.content.replace(f'{moreInfoString}', '').strip()
			toolTipString = removedInfo 
			answerWithContext = removedInfo 
			print('Response with more info removed', removedInfo )
			return toolTipString, None, answerWithContext, None

		# Raw sql query is used to create tool tip that will be displayed on hover of response in front end
		toolTipString = self.getRawSqlQuery(response)

		# Have to put the sql query in " " so it can be executed properly
		formattedSqlQuery = f"{toolTipString}"

		# Formatted db response = string that will be displayed on front end
		# Item urls = name and urls that will be used to create href links in the response on front end
		formattedDbResponse, itemUrls = self.getResponseFromDb(formattedSqlQuery)

		# Give the agent the original prompt so it can answer the original prompt with the data it recieved from db
		answerWithContext = self.provideContextForDbResponse(userPrompt, formattedDbResponse)
		return toolTipString, formattedSqlQuery, answerWithContext, itemUrls


apiKey = os.getenv('OPEN_AI_SECRET_KEY')
llmAgent = LLMAgent(apiKey)