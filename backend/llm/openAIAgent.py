from openai import OpenAI
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
load_dotenv()
import sqlparse
from sql.sqlUtility import getDatabaseSchema, executeSelectQuery


client = OpenAI(api_key=os.getenv('OPEN_AI_SECRET_KEY'))
# Set up your OpenAI API key

def queryAgent(prompt):
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
def createSchemaPrompt(schema):
	prompt = "I have the following tables and columns in my SQL database:\n\n"
	for table, columns in schema.items():
		prompt += f"Table: {table}\nColumns: {', '.join(columns)}\n\n"

	return prompt

def provideContextForDatabaseResponse(originalPrompt, dbResponse):
	context = f"I just asked you this:\n\n{originalPrompt}\n\n"
	answer = f"\nI checked my database and found this answer:\n\n{dbResponse}"
	prompt = context + answer + "\n\nCan you write a sentence answering the original prompt with the result from my database"
	return queryAgent(prompt)

def createSqlQuery(userPrompt):

	dataBaseSchema = getDatabaseSchema()

	schemaPrompt = createSchemaPrompt(dataBaseSchema)

	fullPrompt = schemaPrompt + f"""\n\nHow would you write a MariaDB SQL query to answer this:\n
										{userPrompt}
									\nPlease don't return any context, just the query you would use"""

	response = queryAgent(fullPrompt)
	formmattedResponse = sqlparse.format(response.content, reindent=True, keyword_case='upper')
	rawSqlQuery = formmattedResponse.replace('```sql', '').replace('```', '').strip()

	formattedSqlQuery = f"{rawSqlQuery}" 
	dbResponse = executeSelectQuery(formattedSqlQuery, [])

	formmattedDbResponse = ''
	for key, value in dbResponse['items'][0].items():
		formmattedDbResponse += f"{key}: {value}\n"

	answerWithContext = provideContextForDatabaseResponse(userPrompt, formmattedDbResponse)
	return rawSqlQuery, formattedSqlQuery, answerWithContext.content
