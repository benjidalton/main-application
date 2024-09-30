from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
import subprocess
from datetime import datetime
import os
import re
from blueprints import routes, llmRoutes
load_dotenv()

url_tokens = {
	"DB_USER": os.getenv("APP_ACCESS_DB_USERNAME"),
	"DB_PASS": os.getenv("APP_ACCESS_DB_PASSWORD"),
	"DB_HOST": os.getenv("APP_ACCESS_DB_HOSTNAME"),
	"DB_NAME": os.getenv("APP_ACCESS_DB_DATABASE"),
	"DB_PORT": os.getenv("APP_ACCESS_DB_PORT")
}



app = Flask(__name__)

# Configure the database URI
# Replace the connection string with one for your database.
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{url_tokens["DB_USER"]}:{url_tokens["DB_PASS"]}@localhost:{url_tokens["DB_PORT"]}/{url_tokens["DB_NAME"]}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


cors = CORS(app, resources={r'*': {'origins': '*'}})

app.register_blueprint(routes.routes, name='routes')
app.register_blueprint(llmRoutes.llmRoutes, name='llmRoutes')


@app.route('/notify', methods=['POST'])
def notify():
	## to test:  curl -X POST http://localhost:5111/notify -H "Content-Type: application/json" -d '{"message": "hello"}'
	data = request.json
	print(data['message'])  # Print the notification or handle it as needed
	# Here you could integrate a desktop notification library
	return '', 204

# def checkForUpdates():
# 	# Specify your GitHub repo URL
# 	repo_url = "https://github.com/kcbdalton/baseball-app"
	
# 	# Change to your repository directory
# 	repo_dir = "./baseball_app_copy"
	
# 	try:
# 		# Navigate to the repository directory
# 		subprocess.run(["git", "-C", repo_dir, "fetch"], check=True)
		
# 		# Check if there are changes
# 		result = subprocess.run(["git", "-C", repo_dir, "diff", "HEAD", "origin/main"], stdout=subprocess.PIPE)
		
# 		if result.stdout:
# 			print("Updates found. Pulling changes...")
# 			subprocess.run(["git", "-C", repo_dir, "pull"], check=True)
# 			print("Repository updated successfully.")
# 		else:
# 			print("No updates found.")
	
# 	except subprocess.CalledProcessError as e:
# 		print(f"An error occurred: {e}")



# def print_directory_structure(root_dir, indent=""):
# 	# List all files and directories in the specified directory
# 	for item in os.listdir(root_dir):
# 		path = os.path.join(root_dir, item)
# 		print(indent + item)  # Print the item with the current indentation level
# 		if os.path.isdir(path):  # If the item is a directory, recurse into it
# 			print_directory_structure(path, indent + "    ")

if __name__ == '__main__':
	
	# current_directory = os.getcwd()
	# print(f"Folder structure of: {current_directory}\n")
	# print_directory_structure()
	
	currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	message = f"\n{'*' * 30}\n" \
			f"🚀 App Updated Successfully!\n" \
			f"Updated at: {currentTime}\n" \
			f"{'*' * 30}\n"

	print(message)

	app.run(debug=True, host="localhost", port=5111)
