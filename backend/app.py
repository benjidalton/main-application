from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import datetime, timedelta
import bcrypt
import jwt
import os
from blueprints import routes, llmRoutes
load_dotenv()






DB_USER = os.getenv("APP_ACCESS_DB_USERNAME")
DB_PASS = os.getenv("APP_ACCESS_DB_PASSWORD")
DB_HOST = os.getenv("APP_ACCESS_DB_HOSTNAME")
DB_NAME = os.getenv("APP_ACCESS_DB_DATABASE")
DB_PORT = os.getenv("APP_ACCESS_DB_PORT")
SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)

# Configure the database URI
# Replace the connection string with one for your database.
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASS}@localhost:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# .\venv\Scripts\python -c "import os; print(os.urandom(24).hex())"
app.config['SECRET_KEY'] = SECRET_KEY
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	passwordHash = db.Column(db.String(128), nullable=False)

	def __repr__(self):
		return f'<User {self.username}>'



cors = CORS(app, resources={r'*': {'origins': '*'}})
jwt = JWTManager(app)

app.register_blueprint(routes.routes, name='routes')
app.register_blueprint(llmRoutes.llmRoutes, name='llmRoutes')


@app.route('/register', methods=['POST'])
def register():
	username = request.args.get('username')
	password = request.args.get('password').encode('utf-8')
	hashedPassword = bcrypt.hashpw(password, bcrypt.gensalt())
	
	if User.query.filter_by(username=username).first():
		return jsonify({"message": "Username already exists."}), 400

	newUser = User(username=username, passwordHash=hashedPassword)
	db.session.add(newUser)
	db.session.commit()
	return jsonify({"message": "User registered successfully!"})


@app.route('/login', methods=['POST'])
def login():
	username = request.args.get('username')
	password = request.args.get('password').encode('utf-8')

	print('user name in login route: ', username)
	print('password in login route: ', password)

	user = User.query.filter_by(username=username).first()

	if user and bcrypt.checkpw(password,  user.passwordHash.encode('utf-8')):
		token = jwt.encode({
				'username': username,
				'exp': datetime.now(datetime.timezone.utc) + timedelta(hours=1)
			},
			SECRET_KEY, algorithm='HS256')
		return jsonify({"token": token})
	return jsonify({"message": "Invalid credentials"}), 401


@app.route('/notify', methods=['POST'])
def notify():
	data = request.json
	print(data['message'])
	return '', 204


print("db: ", db)


if __name__ == '__main__':
	
	app.run(debug=True, host="localhost", port=5000)
