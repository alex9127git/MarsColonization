# -*- encoding: utf-8 -*-
import os
import random
from db_methods import fill_tables
from flask import Flask, render_template, request, url_for, redirect
import db_session
from forms import RegisterForm, LoginForm, AddJobForm
from jobs import Jobs
from users import User
from flask_login import LoginManager, login_user, login_required, logout_user

app = Flask(__name__)
app.config["SECRET_KEY"] = str(random.randrange(2 ** 64))
login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(401)
def unauthorized(error):
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    return db_sess.query(User).get(user_id)


@app.route("/")
@app.route("/index")
def root():
    return render_template('base.html', title='Домашняя страница',
                           stylesheet_path=url_for('static', filename='css/style.css'))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   stylesheet_path=url_for('static', filename='css/style.css'),
                                   form=form, message="Пароли не совпадают")
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   stylesheet_path=url_for('static', filename='css/style.css'),
                                   form=form, message="Такой пользователь уже есть")
        # noinspection PyArgumentList
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form,
                           stylesheet_path=url_for('static', filename='css/style.css'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/worklog")
        return render_template('login.html', title="Авторизация", message="Неправильный логин или пароль", form=form,
                               stylesheet_path=url_for('static', filename='css/style.css'))
    return render_template('login.html', title='Авторизация', form=form,
                           stylesheet_path=url_for('static', filename='css/style.css'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/worklog")
@login_required
def worklog():
    return render_template("worklog.html", title="Журнал работы",
                           stylesheet_path=url_for('static', filename='css/style.css'),
                           jobs=db_sess.query(Jobs).all(), users=db_sess.query(User).all())


@app.route("/add_job", methods=["GET", "POST"])
@login_required
def add_job():
    form = AddJobForm()
    if form.validate_on_submit():
        # noinspection PyArgumentList
        job = Jobs(
            job=form.jobdesc.data,
            team_leader=form.teamleader.data,
            work_size=form.duration.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect('/worklog')
    return render_template('add_job.html', title='Добавление задания', form=form,
                           stylesheet_path=url_for('static', filename='css/style.css'))


if __name__ == '__main__':
    db_session.global_init("db/mars_explorer.db")
    db_sess = db_session.create_session()
    fill_tables(db_sess)
    app.run(port=8080, host='127.0.0.1')
