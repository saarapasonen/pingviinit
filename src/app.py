from flask import redirect, render_template, request, jsonify, flash, url_for
from db_helper import reset_db
from repositories.todo_repository import get_cites, create_citation, set_done, check_citation_type
from config import app, test_env


def redirect_to_uusi_viite():
    return redirect(url_for("render_uusi_viite"))

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

@app.route("/uusi_viite", methods=["GET"])
def render_uusi_viite():
    return render_template("uusi_viite.html")

@app.route("/luo-viite", methods=["POST"])
def handle_type():
    content = request.form.get("cite")

    try:
        if not content or content == "valitseviite":
            raise ValueError("Valitse viitetyyppi!")

        tyyppi = check_citation_type(content)
        if tyyppi in ["book", "article", "inproceedings"]:
            return redirect(url_for("render_specific_type", tyyppi=tyyppi))

    except Exception as error:
        flash(str(error))
        return redirect_to_uusi_viite()
    
@app.route("/luo-viite/<tyyppi>")
def render_specific_type(tyyppi):
    if tyyppi == "book":
        return render_template("book.html")
    if tyyppi == "article":
        return render_template("article.html")
    if tyyppi == "inproceedings":
        return render_template("inproceedings.html")

@app.route("/luo-viite2", methods=["POST"])
def cite_creation2():
    tyyppi = request.form.get("type")
    if tyyppi == "book":
        author = request.form.get("author")
        publisher = request.form.get("publisher")
        year = request.form.get("year")
        title = request.form.get("title")
        create_citation(tyyppi, author, publisher, year, title)
    if tyyppi == "article":
        author = request.form.get("author")
        journal = request.form.get("journal")
        year = request.form.get("year")
        title = request.form.get("title")
        create_citation(tyyppi, author, None, year, title, journal)
    if tyyppi == "inproceedings":
        author = request.form.get("author")
        booktitle = request.form.get("booktitle")
        year = request.form.get("year")
        title = request.form.get("title")
        create_citation(tyyppi, author, None, year, title, None, booktitle)
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
