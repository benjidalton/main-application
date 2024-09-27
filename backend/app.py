from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
import os
import re
import blueprints.routes as routes
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
jwt = JWTManager(app)

app.register_blueprint(routes.routes)


if __name__ == '__main__':
	app.run(debug=True, host="localhost", port=5000)
