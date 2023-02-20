# -*- encoding: utf-8 -*-
import os
from flask import Flask, render_template, request, url_for, redirect
import db_session


app = Flask(__name__)
answers_param = dict()


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
    global answers_param
    if request.method == 'GET':
        return render_template('register.html', title='Анкета претендента на участие в миссии',
                               stylesheet_path=url_for('static', filename='css/style.css'))
    elif request.method == 'POST':
        answers_param = {
            "name": request.form.get('name'),
            "surname": request.form.get('surname'),
            "email": request.form.get('email'),
            "education": request.form.get('education'),
            "engineer": request.form.get('engineer') is not None,
            "pilot": request.form.get('pilot') is not None,
            "builder": request.form.get('builder') is not None,
            "nurse": request.form.get('nurse') is not None,
            "sex": request.form.get('sex'),
            "motive": request.form.get('motive'),
            "ready": request.form.get('accept') is not None
        }
        return redirect("/answer")


@app.route("/answer")
def answer():
    global answers_param
    return render_template('answer.html')


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
