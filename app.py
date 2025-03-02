import flask
from flask import Flask, redirect, url_for, flash, render_template, request
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_bcrypt import Bcrypt

from models import db, User
from forms import RegistrationForm, LoginForm
from crud import login_manager
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
    return flask.render_template('/pages/index.html', title='Hello World', content='Hello World!')


# USERS
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Ваш аккаунт был создан! Теперь вы можете войти', 'success')
        return redirect(url_for('index'))
    return render_template('/pages/register.html', title='Регистрация', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
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
