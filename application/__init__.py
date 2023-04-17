from flask import Flask
from flask_pymongo import PyMongo
app = Flask(__name__)
app.config["SECRET_KEY"] = "5f5cd6247a3d8ab132a8bcc5bb13c6148102e193"
app.config["MONGO_URI"] = "mongodb://localhost:27017/gym"

#setup mongoDB
mongodb_client = PyMongo(app)
db = mongodb_client.db



from application import routes

