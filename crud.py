from flask_login import LoginManager

from models import User
from db import db


login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_user(username, hashed_password, email):
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