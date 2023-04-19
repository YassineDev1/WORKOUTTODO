from application import app, mongodb_client
from flask import jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity)
from .models import User, Workout
import json 
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

#Create a Workout
@app.route("/api/workouts", methods=["POST"])
def create_workout():
    json = request.json
    title = json['title']
    reps = json['reps']    
    load = json['load']
    if not title or not reps or not load:
        return jsonify({"error": "Missing fields"}), 400

    workout = Workout(title=title, reps=reps, load=load)
    workout.save()

    return jsonify({"success": "Workout created successfully"}), 201

#All Workouts
@app.route("/api/workouts", methods=["GET"])
def get_workouts():
    all_workouts = mongodb_client.db.workouts.find({},{'_id':0})
    return jsonify({"workouts": [workout for workout in all_workouts]}), 200