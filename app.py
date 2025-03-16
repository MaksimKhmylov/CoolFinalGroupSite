import random
import os

import flask
from flask import Flask, redirect, url_for, flash, render_template, request
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_bcrypt import Bcrypt

from werkzeug.utils import secure_filename

from models import db, User, Place
from forms import RegistrationForm, LoginForm, AddPlaceForm
from crud import login_manager, create_user, get_user_by_email, create_place
from config import Config


UPLOAD_FOLDER = 'static/img/places'
app = Flask(__name__)
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'


@app.route('/')
def index():
    if not Place.query.all():
        return render_template("/pages/no_places.html")
    return render_template('/pages/index.html',
                           places=Place.query.all(),
                           random_place=random.randint(1, len(Place.query.all()))
                           )


@app.route('/random_place')
def random_place():
    if not Place.query.all():
        return render_template("/pages/no_places.html")
    place = Place.query.get(random.randint(1, len(Place.query.all())))
    if not place:
        return render_template("/pages/404.html")
    author = User.query.get(place.author)
    pictures = str(place.picture).replace(" ", "").split(",")
    return render_template('/pages/place.html', place=place, author=author, pictures=pictures)


@app.route('/add_place', methods=['GET', 'POST'])
def add_place():
    if not current_user.is_authenticated:
        return redirect(url_for('register'))
    form = AddPlaceForm()
    if form.validate_on_submit():
        if 'picture' not in request.files:
            flash('Ошибка', 'danger')
        else:
            file = request.files['picture']
            if file.filename == '':
                flash('Нет выбраных файлов', 'danger')
                return redirect(request.url)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            create_place(name=form.name.data,
                         description=form.description.data,
                         country=form.country.data,
                         author=current_user.id,
                         picture=filename,
                         site=form.site.data,
                         position=form.position.data)
            flash("Место создано!", "success")
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
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
