from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date
import sys
from helpers import login_required

# configure app
app = Flask(__name__)   
app.secret_key = "ad601a20df5fcfcb266d8fd89365336f"
# make sqlite3 file work
con = sqlite3.connect("todo.db", check_same_thread=False)
cur = con.cursor()

@app.route("/register", methods=["GET", "POST"])
def register():
    global cur
    if request.method == "POST":
        username = request.form.get("username")
        passnothash = request.form.get("password")
        password = generate_password_hash(request.form.get("password"))
        confirmation = request.form.get("confirmation")
        if confirmation != passnothash:
            return render_template("register.html", errmsg="confirmation does not match")
        try:
            cur.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, password))
        except:
            return render_template("register.html", err_msg="username not unique")
        con.commit()
        return render_template("login.html")
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    today = date.today()
    if request.method.upper() == "POST":
        cur.execute("SELECT * FROM users WHERE username = ?", [request.form.get("username")])
        rows = cur.fetchall()
        data=None
        for row in rows:
            data = row
            break
        if not data:
            return render_template("login.html")
        elif not check_password_hash(data[2], request.form.get("password")):    
            return render_template("login.html")
        # print("going to index", file=sys.stderr)
        session["user_id"] = data[1]
        # cur.execute("SELECT todo, done, id FROM todos WHERE user_id = ?", (session["user_id"]))
        #cur.fetchall()
        todos = query_todos() 
        
        # print("%r" % todos, file=sys.stderr)
        return render_template("index.html", todos=todos)
        # return render_template("index.html")
    else:
        return render_template("login.html")

@login_required
def query_todos():
    
  #  today = date.today()
  #  cur.execute("INSERT INTO todos (date, todo, user_id) VALUES (?, ?, ?)", (today, todo, session["user_id"]))
  #  con.commit()
    print("query_todos - cur = %r" % cur, file=sys.stderr)
    print("SELECT todo, done, id FROM todos WHERE user_id = %r" % session["user_id"], sys.stderr)
    cur.execute("SELECT todo, done, id FROM todos WHERE user_id = ?", (session["user_id"]))

    todos = cur.fetchall()
    return todos

def insert_todo(todo):
    today = date.today()
    cur.execute("INSERT INTO todos (date, todo, user_id) VALUES (?, ?, ?)", (today, todo, session["user_id"]))
    con.commit()

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        todo = request.form.get("todos")
        insert_todo(todo)
    todos = query_todos()

    return render_template("index.html", todos=todos)
    
    
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/record-todos", methods=["POST"])
@login_required
def process_form():

    if request.method == "POST":
        cur.execute("UPDATE todos SET done = 0 WHERE user_id = ?", session["user_id"])
        con.commit()
        done_todos = request.form.getlist("todos")
        
        for todo_id in done_todos:
            cur.execute("UPDATE todos SET done = 1 WHERE id = ?", (todo_id,))
            con.commit()
        todos = query_todos()
        return render_template("index.html", todos=todos)


    return render_template("index.html")