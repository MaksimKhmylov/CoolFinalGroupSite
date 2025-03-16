import os

from flask_login import LoginManager, login_user
from flask import flash, redirect, url_for
from werkzeug.utils import secure_filename

from models import User, Place
from db import db


login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_user(username, email, hashed_password):
    user = User(username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return user


def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    return user


def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    return user

def create_place(name, description, country,author , picture, site, position):
    place = Place(
        name=name, description=description, country=country,
        author=author, picture=picture, site=site, position=position)
    db.session.add(place)
    db.session.commit()
    return place
