from flask import Flask
from flask_sqlalchemy import SQLAlchemy
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




print("Using database connection: ", url_tokens)

app = Flask(__name__)

# Configure the database URI
# Replace the connection string with one for your database.
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{url_tokens["DB_USER"]}:{url_tokens["DB_PASS"]}@localhost:{url_tokens["DB_PORT"]}/{url_tokens["DB_NAME"]}'

# Optional: Track modifications of objects and emit signals
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # Initialize SQLAlchemy with the Flask app
# db = SQLAlchemy(app)

# # Define a model
# class User(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	username = db.Column(db.String(80), unique=True, nullable=False)
# 	email = db.Column(db.String(120), unique=True, nullable=False)

# 	def __repr__(self):
# 		return f'<User {self.username}>'

# Create tables (run once)
# with app.app_context():
	# db.create_all()

app.register_blueprint(routes.routes)


if __name__ == '__main__':
	app.run(debug=True, host="localhost", port=5000)
