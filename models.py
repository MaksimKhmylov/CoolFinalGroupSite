from flask_login import UserMixin
from db import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    # places = db.relationship('Place', backref='owner', lazy=True)
    # comments = db.relationship('Comment', backref='owner', lazy=True)


class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    country = db.Column(db.String(120), nullable=False)
    author = db.Column(db.Integer, db.ForeignKey('user.id'))
    picture = db.Column(db.String(120))
    site = db.Column(db.String(120))
    position = db.Column(db.String(120))
    # comments = db.relationship('Comment', backref='place', lazy=True)


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(120), unique=True, nullable=False)
    rate = db.Column(db.Integer, unique=True, nullable=False)
    author = db.Column(db.Integer, db.ForeignKey('user.id'))
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))
