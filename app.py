from flask import Flask, render_template, url_for, redirect
from instance.config import SECRET_KEY
from flask_bootstrap import Bootstrap

app = Flask(__name__, instance_relative_config=True)
Bootstrap(app)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("finances.html")

@app.route('/income')
def income():
    return render_template("income.html")

@app.route('/notes')
def notes():
    return render_template("notes.html")


if __name__ == '__main__':
    app.run(debug=True)
