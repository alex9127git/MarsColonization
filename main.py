from flask import Flask, render_template
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
    app.run(port=8080, host='127.0.0.1')
