# -*- encoding: utf-8 -*-

from flask import Flask, render_template
import db_session
from users import User
from jobs import Jobs
app = Flask(__name__)


@app.route("/")
def root():
    return render_template('base.html', title='Домашняя страница')


@app.route("/index")
def index():
    return "И на Марсе яблони будут цвести!"


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


@app.route("/registration_form")
def registration_form():
    with open("static/html/form.html", "r", encoding="utf-8") as file:
        return file.read()


if __name__ == '__main__':
    db_session.global_init("db/mars_explorer.db")
    db_sess = db_session.create_session()
    user = User()
    user.surname = "Scott"
    user.name = "Ridley"
    user.age = 21
    user.position = "captain"
    user.speciality = "research engineer"
    user.address = "module_1"
    user.email = "scott_chief@mars.org"
    user.hashed_password = "cap"
    db_sess.add(user)
    job = Jobs()
    job.team_leader = 1
    job.job = 'deployment of residential modules 1 and 2'
    job.work_size = 15
    job.collaborators = '2, 3'
    job.is_finished = False
    db_sess.add(job)
    db_sess.commit()
    app.run(port=8080, host='127.0.0.1')
