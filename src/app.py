from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from repositories.todo_repository import get_todos, create_citation, set_done
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

@app.route("/lisatyt")
def lisatyt():
    return render_template("lisatyt.html")

@app.route("/luo-viite", methods=["POST"])
def cite_creation():
    content = request.form.get("cite")
    if content == "book":
       return render_template("book.html")
    elif content == "article":
       return render_template("article.html")
    elif content == "inproceedings":
       return render_template("inproceedings.html")

@app.route("/luo-viite2", methods=["POST"])
def cite_creation2():
    type = request.form.get("type")
    if type == "book":
        author = request.form.get("author")
        publisher = request.form.get("publisher")
        year = request.form.get("year")
        title = request.form.get("title")
        create_citation(type, author, publisher, year, title)
    if type == "article":
        author = request.form.get("author")
        journal = request.form.get("journal")
        year = request.form.get("year")
        title = request.form.get("title")
        create_citation(type, author, None, year, title, journal)
    if type == "inproceedings":
        author = request.form.get("author")
        booktitle = request.form.get("booktitle")
        year = request.form.get("year")
        title = request.form.get("title")
        create_citation(type, author, None, year, title, None, booktitle)
    return redirect("/")


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
