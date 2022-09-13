from flask import Flask, render_template

app = Flask(__name__)

app.config.from_pyfile("config.py")


@app.route("/home")
def home():
    return render_template("principal.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route("/login")
def login():
    return render_template("login.html")