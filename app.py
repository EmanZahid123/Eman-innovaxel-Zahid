from flask import Flask, request, jsonify, redirect
from flask_pymongo import PyMongo
from datetime import datetime
import string, random


app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize MongoDB connection
mongo = PyMongo(app)
db = mongo.db
