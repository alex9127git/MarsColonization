# -*- encoding: utf-8 -*-
import os
import random
from db_methods import fill_tables
from flask import Flask, render_template, request, url_for, redirect
import db_session
from forms import RegisterForm, LoginForm
from jobs import Jobs
from users import User
from flask_login import LoginManager, login_user

app = Flask(__name__)
app.config["SECRET_KEY"] = str(random.randrange(2 ** 64))
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db_sess.query(User).get(user_id)


@app.route("/")
@app.route("/index")
def root():
    return render_template('base.html', title='Домашняя страница',
                           stylesheet_path=url_for('static', filename='css/style.css'))


@app.route("/list_prof/<list_type>")
def list_prof(list_type):
    return render_template('profession_list.html', title='Список профессий', list_type=list_type,
                           stylesheet_path=url_for('static', filename='css/style.css'))


@app.route("/promotion")
def promotion():
    return "</br>".join(("Человечество вырастает из детства.",
                         "Человечеству мала одна планета.",
                         "Мы сделаем обитаемыми безжизненные пока планеты.",
                         "И начнем с Марса!",
                         "Присоединяйся!"))


@app.route("/image_mars")
def image_mars():
    with open("static/html/image_mars.html", "r", encoding="utf-8") as file:
        return file.read()


@app.route("/promotion_image")
def promotion_image():
    with open("static/html/promotion_image.html", "r", encoding="utf-8") as file:
        return file.read()


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


@app.route("/register_success")
def register_success():
    return render_template('register_success.html', title='Успешная регистрация',
                           stylesheet_path=url_for('static', filename='css/style.css'))


@app.route("/distribution")
def distribution():
    return render_template('distribution.html',
                           title="Расположение персонала в каютах",
                           stylesheet_path=url_for('static', filename='css/style.css'),
                           members=["Readley Scott", "Andy Weer", "Mark Woatney",
                                    "Wenkata Kapoor", "Teddy Sanders", "Shong Bing"])


@app.route("/load_photo", methods=["GET", "POST"])
def load_photo():
    with open("static/html/load_photo.html", "r", encoding="utf-8") as file:
        if request.method == "GET":
            return file.read().replace("{img}", "")
        if request.method == "POST":
            imgdata = request.files["file"]
            if not os.path.exists("static/tmp"):
                os.mkdir("static/tmp")
            with open("static/tmp/tmp.png", "wb") as image:
                image.write(imgdata.read())
            return file.read().replace("{img}", '<img src="static/tmp/tmp.png" alt="">')


@app.route("/mars_carousel")
def mars_carousel():
    with open(f"static/html/mars_carousel.html", "r", encoding="utf-8") as file:
        return file.read()


@app.route("/choice/<planet_name>")
def choice(planet_name):
    planet_name = planet_name.lower()
    if planet_name == "марс":
        planet_name = "mars"
    if planet_name == "венера":
        planet_name = "venus"
    with open(f"static/html/{planet_name.lower()}.html", "r", encoding="utf-8") as file:
        return file.read()


@app.route("/results/<nickname>/<int:level>/<float:rating>")
def results(nickname, level, rating):
    with open(f"static/html/results.html", "r", encoding="utf-8") as file:
        contents = file.read()
        contents = contents.replace("{nickname}", nickname).replace("{level}", str(level)).\
            replace("{rating}", str(rating))
        return contents


@app.route("/worklog")
def worklog():
    return render_template("worklog.html", title="Журнал работы",
                           stylesheet_path=url_for('static', filename='css/style.css'),
                           jobs=db_sess.query(Jobs).all(), users=db_sess.query(User).all())


if __name__ == '__main__':
    db_session.global_init("db/mars_explorer.db")
    db_sess = db_session.create_session()
    fill_tables(db_sess)
    app.run(port=8080, host='127.0.0.1')
