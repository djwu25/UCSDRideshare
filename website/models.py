from datetime import datetime
from enum import unique
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    posts = db.relationship('Post')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    depart_from = db.Column(db.String(100), nullable=False)
    arrive_to = db.Column(db.String(100), nullable=False)
    seats_available = db.Column(db.Integer, nullable=False)
    seat_cost = db.Column(db.Integer, nullable=False)
    time_of_departure = db.Column(db.Time, nullable=False)
    date_of_departure = db.Column(db.Date, nullable=False)
    extra_info = db.Column(db.Text, nullable=False)

