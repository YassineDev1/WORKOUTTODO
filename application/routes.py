# Import required libraries
from application import app, mongodb_client
from flask import jsonify, request, abort
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity)
from .models import User, Workout
from flask_bcrypt import generate_password_hash
from flask_cors import cross_origin 


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
        token_expires_in = app.config['JWT_ACCESS_TOKEN_EXPIRES'].total_seconds()
        return jsonify({
            "data": user.to_json(),
            "accessToken": access_token,
            "refreshToken" : refresh,
            "tokenExpiresIn": token_expires_in
        }), 200
    return jsonify({"message": "Invalid email or password"}), 401

@app.route("/api/users/refresh-token", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify({"accessToken": access_token}), 200
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
        return jsonify({"message": "Email already exists", "status":404})

    hashed_password = generate_password_hash(password).decode('utf-8')

    user = User(name, email, hashed_password)
    mongodb_client.db.users.insert_one({"name": user.name, "email": user.email, "password": user.password})

    access_token = create_access_token(identity=user.email)
    refresh_token = create_refresh_token(identity=user.email)

    return jsonify({
        "message" : "Registred Successfully",
        "accessToken": access_token,
        "refreshToken": refresh_token
    }), 201

# Workout routes
@app.route('/workouts', methods=['POST'])
@cross_origin()
@jwt_required()
def create_workout():
    user_id = get_jwt_identity()
    title = request.json.get('title')
    reps = request.json.get('reps')
    load = request.json.get('load')

    if not title or not reps or not load:
        abort(400)

    workout = Workout(user_id=user_id, title=title, reps=reps, load=load)
    workout.save()

    return jsonify(workout=workout.to_json()), 201



#All Workouts
@app.route("/api/workouts", methods=["GET"])
@cross_origin()
@jwt_required()
def get_workouts():
    user_id = get_jwt_identity()
    workouts = Workout.find_by_user_id(user_id)

    serialized_workouts = []
    for workout in workouts:
        serialized_workout = {
            "_id": str(workout._id),
            "title": workout.title,
            "reps": workout.reps,
            "load": workout.load,
            "createdAt": workout.created_at
        }
        serialized_workouts.append(serialized_workout)

    return jsonify(workouts=serialized_workouts), 200


#Single Workout
@app.route('/api/workouts/<workout_id>', methods=['GET'])
@cross_origin()
@jwt_required()
def get_workout(workout_id):
    workout = Workout.find_by_id(workout_id)
    if not workout:
        abort(404) 
    return jsonify(workout=workout.to_json())

#Update Workout
@app.route('/api/workouts/<workout_id>', methods=['PUT'])
@cross_origin()
@jwt_required()
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
@cross_origin()
@jwt_required()
def delete_workout(workout_id):
    workout = Workout.find_by_id(workout_id)
    if not workout:
        abort(404)
    workout.delete()
    return jsonify({"message": "Workout Deleted"}), 204