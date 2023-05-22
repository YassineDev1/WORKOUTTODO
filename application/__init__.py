from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from datetime import timedelta

app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = "5f5cd6247a3d8ab132a8bcc5bb13c6148102e193"
app.config["MONGO_URI"] = "mongodb://localhost:27017/gym"
app.config["JWT_SECRET_KEY"] = "yassinedev1"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=1)
app.config["HOST"] = "http://localhost:3000"
app.config['CORS_HEADERS'] = 'Content-Type'
#setup mongoDB
mongodb_client = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

from application import routes