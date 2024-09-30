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

def provideContextForDbResponse(originalPrompt, dbResponse):
	context = f"I just asked you this:\n\n{originalPrompt}\n\n"
	answer = f"\nI checked my database and found this answer:\n\n{dbResponse}"
	prompt = context + answer + "\n\nCan you write a sentence answering the original prompt with the result from my database"
	return queryAgent(prompt).content


def getRawSqlQuery(response): 
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


def createSqlQuery(userPrompt, promptType):
	if promptType != 'DB Query':
		print('you didnt  have db query chosen')
		return
	
	dataBaseSchema = getDatabaseSchema()
	
	schemaPrompt = createSchemaPrompt(dataBaseSchema)

	moreInfoString = 'MORE INFORMATION NEEDED'
	fullPrompt = schemaPrompt + f"""\n\nHow would you write a MariaDB SQL query to answer this:\n
										{userPrompt}
									\nPlease don't return any context, just the query you would use. 
									It is imperative you provide any url references from the database applicable to the items in the response.
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