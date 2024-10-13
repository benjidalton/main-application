from openai import OpenAI
import json
import os
import sys
import sqlparse
from dotenv import load_dotenv
load_dotenv()
# custom imports
import services.sql.sql_utility as sql_utility
APP_ACCESS_BASEBALL_DB = os.getenv('APP_ACCESS_BASEBALL_DB')
class LLMAgent:
	def __init__(self, apiKey: str):
		self.client = OpenAI(api_key=apiKey)

	def query_agent(self, prompt: str):
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

			print('response in query_agent to check the typing of the response: ', response.choices[0].message)

			return response.choices[0].message


	def create_schema_prompt(self, schema: dict) -> str:
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


	def provide_context_for_db_response(self, original_prompt: str, db_response: str) -> str:
		"""
			Creates a contextual prompt for the AI model based on the original question and database response.

			Args:
				original_prompt (str): * The user's original question.
				db_response (str): * The answer retrieved from the database.

			Returns:
				str: The AI-generated sentence that answers the original prompt using the database response.
		"""
		context = f"I just asked you this:\n\n{original_prompt}\n\n"
		answer = f"\nI checked my database and found this answer:\n\n{db_response}"
		prompt = context + answer + "\n\nCan you write a sentence answering the original prompt with the result from my database?"
		return self.query_agent(prompt).content


	def get_raw_sql_query(self, response) -> str:
		"""Formats and cleans the SQL response from the AI model."""
		formatted_response = sqlparse.format(response.content, reindent=True, keyword_case='upper')
		return formatted_response.replace('```sql', '').replace('```', '').strip()


	def get_response_from_db(self, formatted_sql_query) -> tuple:
		"""Executes the SQL query and retrieves the response from the database."""
		db_response = sql_utility.execute_select_query(APP_ACCESS_BASEBALL_DB, formatted_sql_query, [])
		print('db response: ', db_response)

		item_urls = [
			{'name': item['name'], 'baseball_reference_url': item['baseballReferenceUrl']} 
			if 'baseballReferenceUrl' in item 
			else None
			for item in db_response['items'] 
		]

		formatted_db_response = ''
		for item in db_response['items']:
			for key, value in item.items():
				if key == 'baseballReferenceUrl':
					continue
				formatted_db_response += f"{key}: {value}\n"
			formatted_db_response += "\n"

		return formatted_db_response, item_urls


	def create_sql_query(self, user_prompt: str, prompt_type: str) -> tuple:
		"""
			Generates a MariaDB SQL query based on the user's prompt and the database schema.

			Args:
				user_prompt (str): * The user's question or request for an SQL query.
				prompt_type (str): * The type of the prompt, expected to be 'DB Query'.

			Returns:
				tuple: A tuple containing:
					- tool_tip_string (str): A string with additional information if needed.
					- formatted_sql_query (str or None): The generated SQL query or None if not applicable.
					- answer_with_context (str): Contextual information about the query result.
					- item_urls (list or None): Any applicable URLs from the database.
		"""
		if prompt_type != 'DB Query':
			print('You did not have DB Query chosen')
			return

		# Load database schema
		database_schema = sql_utility.get_database_schema()
		schema_prompt = self.create_schema_prompt(database_schema)

		more_info_string = 'MORE INFORMATION NEEDED'
		full_prompt = schema_prompt + f"""\n\nHow would you write a MariaDB SQL query to answer this:\n
										{user_prompt}
									\nPlease don't return any context, just the query you would use. 
									It is imperative you provide any URL references from the database applicable to the items in the response.
									\nDon't include qualifiers like 'player' or 'team' when defining values in the query. For example, if I ask you for the name
									of the team with the most home runs, just use the 'teams' table and the 'name' column. 
									\nMake sure to select the data that would help with answering the prompt so it can be used to provide more context.
									\n\n If you don't think you can answer the question with the database schema provided, provide information on what I can add to my 
										database schema that would help you. Start your response with {more_info_string} in all caps so I can handle it. """

		response = self.query_agent(full_prompt)

		if more_info_string in response.content:
			print('More info needed for response')
			removed_info = response.content.replace(f'{more_info_string}', '').strip()
			tool_tip_string = removed_info 
			answer_with_context = removed_info 
			print('Response with more info removed', removed_info )
			return tool_tip_string, None, answer_with_context, None

		tool_tip_string = self.get_raw_sql_query(response)

		formatted_sql_query = f"{tool_tip_string}"

		formatted_db_response, item_urls = self.get_response_from_db(formatted_sql_query)

		answer_with_context = self.provide_context_for_db_response(user_prompt, formatted_db_response)
		return tool_tip_string, formatted_sql_query, answer_with_context, item_urls


api_key = os.getenv('OPEN_AI_SECRET_KEY')
llm_agent = LLMAgent(api_key)



	