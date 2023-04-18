from application import  mongodb_client
from flask_bcrypt import generate_password_hash, check_password_hash
class User:
    def __init__(self,name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    @staticmethod
    def find_by_email(email):
        user = mongodb_client.db.users.find_one({"email": email})
        if not user:
            return None
        return User(user["name"], user["email"], user["password"])

    