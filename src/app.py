from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from repositories.todo_repository import get_todos, create_todo, set_done
from config import app, test_env
from util import validate_todo

@app.route("/")
def index():
    todos = get_todos()
    unfinished = len([todo for todo in todos if not todo.done])
    return render_template("index.html", todos=todos, unfinished=unfinished)

@app.route("/uusi-viite")
def new():
    return render_template("uusi_viite.html")

@app.route("/luo-viite", methods=["POST"])
def cite_creation():
    content = request.form.get("cite")
    print(content)
    if content == "book":
       return render_template("book.html")
    elif content == "article":
       return render_template("article.html")
    elif content == "inproceedings":
       return render_template("inproceedings.html")
    
    


@app.route("/toggle_todo/<todo_id>", methods=["POST"])
def toggle_todo(todo_id):
    set_done(todo_id)
    return redirect("/")

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
