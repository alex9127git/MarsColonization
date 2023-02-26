from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта (используется как логин)', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    age = StringField('Возраст', validators=[DataRequired()])
    position = StringField('Ранг', validators=[DataRequired()])
    speciality = StringField('Должность', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    submit = SubmitField('Завершить регистрацию')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class AddJobForm(FlaskForm):
    jobdesc = StringField('Описание задания', validators=[DataRequired()])
    teamleader = StringField('ID лидера задания', validators=[DataRequired()])
    duration = StringField('Продолжительность', validators=[DataRequired()])
    collaborators = StringField('ID помощников', validators=[DataRequired()])
    is_finished = BooleanField('Завершено')
    submit = SubmitField('Добавить задание')
