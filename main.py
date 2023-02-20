# -*- encoding: utf-8 -*-
import os
from flask import Flask, render_template, request
import db_session


app = Flask(__name__)


@app.route("/")
@app.route("/index")
def root():
    return render_template('base.html', title='Домашняя страница')


@app.route("/list_prof/<list_type>")
def list_prof(list_type):
    return render_template('profession_list.html', title='Список профессий', list_type=list_type)


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


if __name__ == '__main__':
    db_session.global_init("db/mars_explorer.db")
    db_sess = db_session.create_session()
    app.run(port=8080, host='127.0.0.1')
