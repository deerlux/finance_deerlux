from flask import Flask
from dataModels import *
app = Flask(__name__)
app.config.from_object('config')

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from app import views

