from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from datetime import timedelta
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)

# Load environment variables from .env file
load_dotenv('.flaskenv')

# Configure the Flask application
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["HOST"] = os.environ.get("HOST", "http://localhost:3000")
app.config['CORS_HEADERS'] = 'Content-Type'

# Setup MongoDB
mongodb_client = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

from application import routes
