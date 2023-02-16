# -*- encoding: utf-8 -*-
from flask import Flask, render_template, request
import db_session


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


@app.route("/load_photo", methods=["GET", "POST"])
def load_photo():
    with open("static/html/load_photo.html", "r", encoding="utf-8") as file:
        if request.method == "GET":
            return file.read().replace("{src}", "")
        if request.method == "POST":
            img = request.files["file"]
            return file.read().replace("{src}", img.read())


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


if __name__ == '__main__':
    db_session.global_init("db/mars_explorer.db")
    db_sess = db_session.create_session()
    app.run(port=8080, host='127.0.0.1')
