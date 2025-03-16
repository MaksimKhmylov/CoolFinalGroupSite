from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from crud import get_user_by_username, get_user_by_email


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя (2-20 символов)', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = get_user_by_username(username.data)
        if user:
            raise ValidationError('Это имя пользователя уже занято. Пожалуйста, выберите другое.')

    def validate_email(self, email):
        user = get_user_by_email(email.data)
        if user:
            raise ValidationError('Этот email уже занят. Пожалуйста, выберите другой.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Войти")

class AddPlaceForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    country = StringField('Страна', validators=[DataRequired()])
    author = StringField('ID пользователя')
    picture = FileField('Picture', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    site = StringField('Сайт', validators=[DataRequired()])
    position = StringField('Местоположение', validators=[DataRequired()])
    submit = SubmitField("Добавить")