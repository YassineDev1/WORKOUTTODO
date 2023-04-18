from application import app
from flask import jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity)
from .models import User
@app.route("/")

def index():
    return "Hello"

#login
@app.route("/login", methods=["POST"])

def login():
    json = request.json
    email = json['email']
    password = json['password']

    user = User.find_by_email(email)

    if not user and not User.check_password(password):
        return jsonify({"message": "Invalid Email or Password"},401)
    access_token = create_access_token(identity=user.email)
    refresh = create_refresh_token(identity=user.email)

    return jsonify({
        "access-token": access_token,
        "refresh-toke" : refresh
    }, 200)