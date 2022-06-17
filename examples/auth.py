from flask import Blueprint, app, request, jsonify
from src.constants.status_codes import *
from werkzeug.security import check_password_hash, generate_password_hash
from src.constants.responses import *



auth = Blueprint("auth",__name__, url_prefix="/api/v1/auth")

@auth.post('/register')
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if len(password) < 6:
        return jsonify({'error': "Password is too short"}), HTTP_400_BAD_REQUEST

    if len(username) < 3:
        return jsonify({'error': "User is too short"}), HTTP_400_BAD_REQUEST

    if not username.isalnum() or " " in username:
        return jsonify({'error': "Username should be alphanumeric, also no spaces"}), HTTP_400_BAD_REQUEST

    pwd_hash = generate_password_hash(password)

    return jsonify({
        'message': "User created",
        'user': {
            'username': username, 
			"email": email,
			"password_generated": pwd_hash,
      'message_two': dict(english['error']).get('BLOCKED_USER')
    }

    }), HTTP_201_CREATED

@auth.get("/me")
def me():
	return {"user": "me"}