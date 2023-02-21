from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# configure app
app = Flask(__name__)

# make sqlite3 file work
con = sqlite3.connect("todo.db")
cur = con.cursor()

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))
        cur.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, password)
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        rows = cur.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return 1
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template(login.html)
        

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        todo = request.form.get("todo")
        cur.execute("INSERT INTO todos (date, todo, user_id) VALUES (?, ?, ?)", date, todo, user_id)
    else:
        return render_template("index.html")
