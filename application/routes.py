from application import app, mongodb_client
from flask import jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity)
from .models import User
@app.route("/")

def index():
    return "Hello"

#login
@app.route("/api/users/login", methods=["POST"])

def login():
    json = request.json
    email = json['email']
    password = json['password']

    user = User.find_by_email(email)

    if not user and not User.check_password(password):
        return jsonify({"message": "Invalid Email or Password"}),401
    access_token = create_access_token(identity=user.email)
    refresh = create_refresh_token(identity=user.email)

    return jsonify({
        "access-token": access_token,
        "refresh-toke" : refresh
    }), 200

#Sign Up
@app.route("/api/users/signup", methods=["POST"])

def register():
    json = request.json
    name = json['name']
    email = json['email']
    password = json['password']

    if not name :
        return jsonify({"message": "name is required"})
    if not email :
        return jsonify({"message": "email is required"})
    if not password :
        return jsonify({"message": "password is required"})
    
    existing_user = User.find_by_email(email)

    if not existing_user :
        user = User(name, email, password)
        mongodb_client.db.users.insert_one({"name": user.name, "email": user.email, "password": user.password})
        access_token = create_access_token(identity=user.email)
        refresh = create_refresh_token(identity=user.email)

        return jsonify({
            "access-token": access_token,
            "refresh-token": refresh
        })
    return jsonify({"message": "Email Already Exist"})