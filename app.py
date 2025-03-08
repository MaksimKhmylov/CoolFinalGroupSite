import flask
from flask import Flask, redirect, url_for, flash, render_template, request
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from sqlalchemy.sql.functions import random
import random

from models import db, User, Place
from forms import RegistrationForm, LoginForm, AddPlaceForm
from crud import login_manager, create_user, get_user_by_email, create_place
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'


@app.route('/')
def index():
    return render_template('/pages/index.html',
                           places=Place.query.all(),
                           random_place=random.randint(1, len(Place.query.all()))
                           )
@app.route('/add_place', methods=['GET', 'POST'])
def add_place():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    form = AddPlaceForm()
    if form.validate_on_submit():
        create_place(name=form.name.data,
                     description=form.description.data,
                     country=form.country.data,
                     author=current_user.id,
                     pictures=form.pictures.data,
                     site=form.site.data,
                     position=form.position.data)
        return redirect(url_for('index'))
    return render_template('/pages/add_place.html', title='Добавить Место', form=form)
@app.route('/<int:place_id>')
def place(place_id):
    place = Place.query.get(place_id)
    if not place:
        return render_template("/pages/404.html")
    author = User.query.get(place.author)
    pictures = str(place.picture).replace(" ", "").split(",")
    return render_template('/pages/place.html', place=place, author=author, pictures=pictures)


# USERS
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        create_user(username=form.username.data, email=form.email.data, hashed_password=hashed_password)
        flash('Ваш аккаунт был создан! Теперь вы можете войти', 'success')
        return redirect(url_for('login'))
    return render_template('/pages/register.html', title='Регистрация', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_email(form.email.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            return redirect(url_for('index'))
        else:
            flash('Неудачный вход. Пожалуйста, проверьте email и пароль', 'danger')
    return render_template('/pages/login.html', title='Вход', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
