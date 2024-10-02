from flask import Blueprint, jsonify, request
import bcrypt
import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
load_dotenv()

#custom imports 
from models import User

SECRET_KEY = os.getenv("SECRET_KEY")
loginRoutes = Blueprint('loginRoutes', __name__, template_folder='templates')

@loginRoutes.route('/register', methods=['POST'])
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


@loginRoutes.route('/login', methods=['POST'])
def login():
	username = request.json['username']
	password = request.json['password'].encode('utf-8')

	print('user name in login route: ', username)
	print('password in login route: ', password)

	user = User.query.filter_by(username=username).first()

	if username in users_db and bcrypt.checkpw(password,  user.passwordHash.encode('utf-8')):
		token = jwt.encode({
				'username': username,
				'exp': datetime.now(datetime.timezone.utc) + timedelta(hours=1)
			},
			SECRET_KEY, algorithm='HS256')
		return jsonify({"token": token})
	return jsonify({"message": "Invalid credentials"}), 401