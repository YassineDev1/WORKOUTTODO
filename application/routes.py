# Import required libraries
from application import app, mongodb_client
from flask import jsonify, request, abort
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity)
from .models import User, Workout
from flask_bcrypt import generate_password_hash


# Default route
@app.route("/")
def index():
    return "Hello"

# User authentication
@app.route("/api/users/login", methods=["POST"])
def login():
    json = request.json
    email = json['email']
    password = json['password']

    user = User.find_by_email(email)

    if user and user.check_password(password):
        access_token = create_access_token(identity=user.email)
        refresh = create_refresh_token(identity=user.email)
        return jsonify({
            "access-token": access_token,
            "refresh-token" : refresh
        }), 200
    return jsonify({"message": "Invalid email or password"})

# User registration
@app.route("/api/users/signup", methods=["POST"])
def register():
    json = request.json
    name = json['name']
    email = json['email']
    password = json['password']

    if not name :
        return jsonify({"message": "name is required"}), 400
    if not email :
        return jsonify({"message": "email is required"}), 400
    if not password :
        return jsonify({"message": "password is required"}), 400
    
    existing_user = User.find_by_email(email)

    if existing_user:
        return jsonify({"message": "Email already exists"}), 400

    hashed_password = generate_password_hash(password).decode('utf-8')

    user = User(name, email, hashed_password)
    mongodb_client.db.users.insert_one({"name": user.name, "email": user.email, "password": user.password})

    access_token = create_access_token(identity=user.email)
    refresh_token = create_refresh_token(identity=user.email)

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 201

# Workout routes
@app.route('/workouts', methods=['POST'])
def create_workout():
    title = request.json.get('title')
    reps = request.json.get('reps')
    load = request.json.get('load')
    if not title or not reps or not load:
        abort(400)  # Bad request
    workout = Workout(title=title, reps=reps, load=load)
    workout.save()
    return jsonify(workout=workout.to_json()), 201  # Created


#All Workouts
@app.route("/api/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.find_all()
    return jsonify(workouts=[workout.to_json() for workout in workouts])

#Single Workout
@app.route('/api/workouts/<workout_id>', methods=['GET'])
def get_workout(workout_id):
    workout = Workout.find_by_id(workout_id)
    if not workout:
        abort(404) 
    return jsonify(workout=workout.to_json())

#Update Workout
@app.route('/api/workouts/<workout_id>', methods=['PUT'])
def update_workout(workout_id):
    workout = Workout.find_by_id(workout_id)
    if not workout:
        abort(404) 
    title = request.json.get('title')
    reps = request.json.get('reps')
    load = request.json.get('load')
    if title:
        workout.title = title
    if reps:
        workout.reps = reps
    if load:
        workout.load = load
    workout.save()
    return jsonify(workout=workout.to_json())

#Delete Workout
@app.route('/api/workouts/<workout_id>', methods=['DELETE'])
def delete_workout(workout_id):
    workout = Workout.find_by_id(workout_id)
    if not workout:
        jsonify({"message": "No Workout with this id"}), 404
    workout.delete()
    return jsonify({"message": "Workout Deleted"}), 204

















# Create a new workout
# @app.route("/api/workouts", methods=["POST"])
# def create_workout():
#     json = request.json
#     title = json['title']
#     reps = json['reps']    
#     load = json['load']
#     if not title or not reps or not load:
#         return jsonify({"error": "Missing fields"}), 400

#     workout = Workout(title=title, reps=reps, load=load)
#     workout.save()

#     return jsonify({"success": "Workout created successfully"}), 201

# # Retrieve all workouts
# @app.route("/api/workouts", methods=["GET"])
# def get_workouts():
#     workouts = mongodb_client.db.workouts.find({})
#     all_workouts = []
#     for workout in workouts:
#         workout['_id'] = str(workout['_id'])
#         all_workouts.append(workout)
#     return jsonify({"workouts": [workout for workout in all_workouts]}), 200

# # Retrieve a single workout
# @app.route("/api/workouts/<string:workout_id>", methods=["GET"])
# def get_single_workout(workout_id):
#     print(workout_id)
#     w_id = ObjectId(workout_id)
#     workout = mongodb_client.db.workouts.find_one({"_id": w_id})
#     if not workout :
#         return jsonify({"message": "Workout not found"})
#     workout['_id'] = str(workout['_id'])
#     return jsonify
