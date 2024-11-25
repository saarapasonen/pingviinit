from flask import redirect, render_template, request, jsonify, flash, url_for
from db_helper import reset_db
from repositories.todo_repository import get_cites, create_citation, set_done, check_citation_type
from config import app, test_env


def redirect_to_uusi_viite():
    return redirect(url_for("render_luo_viite"))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/uusi-viite")
def new():
    return render_template("uusi_viite.html")


@app.route("/lisatyt")
def lisatyt():
    cites = get_cites()
    return render_template("lisatyt.html", cites=cites)


@app.route("/luo-viite", methods=["GET"])
def render_luo_viite():
    return render_template("uusi_viite.html")


@app.route("/luo-viite", methods=["POST"])
def handle_type():
    content = request.form.get("cite")

    try:
        if not content or content == "valitseviite":
            raise ValueError("Valitse viitetyyppi!")

        tyyppi = check_citation_type(content)
        if tyyppi == "book":
            return render_template("book.html")
        if tyyppi == "article":
            return render_template("article.html")
        if tyyppi == "inproceedings":
            return render_template("inproceedings.html")

    except Exception as error:
        flash(str(error))
        return redirect_to_uusi_viite()


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


@app.route("/bibtex")
def bibtex():
    cites = get_cites()
    return render_template("bibtex.html", cites=cites)


# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({'message': "db reset"})
