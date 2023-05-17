from application import  mongodb_client
from bson import ObjectId
from flask_bcrypt import check_password_hash

class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def find_by_email(email):
        user = mongodb_client.db.users.find_one({"email": email})
        if not user:
            return None
        return User(user["name"], user["email"], user["password"])
    def to_json(self):
        return {
            "name": self.name,
            "email": self.email,
        }

class Workout:
    def __init__(self, title, reps, load):
        self.title = title
        self.reps = reps
        self.load = load

    def to_json(self):
        return {
            "title": self.title,
            "reps": self.reps,
            "load": self.load
        }
    
    @staticmethod
    def from_json(json):
        workout = Workout(json['title'], json['reps'], json['load'])
        if '_id' in json:
            workout._id = ObjectId(json['_id'])
        return workout

    def save(self):
        workouts = mongodb_client.db.workouts
        if hasattr(self, '_id'):
            workouts.replace_one({'_id': self._id}, self.to_json())
        else:
            result = workouts.insert_one(self.to_json())
            self._id = result.inserted_id

    @staticmethod
    def find_all():
        workouts = mongodb_client.db.workouts.find({})
        return [Workout.from_json(workout) for workout in workouts]

    @staticmethod
    def find_by_id(workout_id):
        w_id = ObjectId(workout_id)
        workout = mongodb_client.db.workouts.find_one({"_id": w_id})
        if not workout:
            return None
        return Workout.from_json(workout)

    def delete(self):
        if hasattr(self, '_id'):
            mongodb_client.db.workouts.delete_one({'_id': self._id})
