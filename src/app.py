import datetime
from flask import redirect, render_template, request, jsonify, flash, url_for, Response
from db_helper import reset_db
from repositories.todo_repository import get_cites, create_citation, check_citation_type
from config import app, test_env

def redirect_to_uusi_viite():
    return redirect(url_for("render_uusi_viite"))

def redirect_to_sama_viite(tyyppi):
    return redirect(url_for("render_specific_type", tyyppi=tyyppi))


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
        if tyyppi not in ["book", "article", "inproceedings"]:
            raise ValueError("Vääränlainen viitetyyppi!")
        return redirect(url_for("render_specific_type", tyyppi=tyyppi))

    except ValueError as error:
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
    return redirect_to_uusi_viite()

@app.route("/luo-viite2", methods=["POST"])
def cite_creation2():
    tyyppi = request.form.get("type")
    vuosi = datetime.date.today().year
    try:
        if tyyppi == "book":
            author = request.form.get("author")
            publisher = request.form.get("publisher")
            year = request.form.get("year")
            title = request.form.get("title")
            if not author or not publisher or not year or not title:
                raise ValueError("Täytä kaikki kentät")
            if len(author) > 500 or len(publisher) > 500 or len(title) > 500:
                raise ValueError("Yhteen kenttään voi kirjoittaa max. 500 merkkiä")
            if int(year) > vuosi or year.isnumeric() is False:
                raise ValueError("Vuosiluvut 0-nykypäivä ovat sallittuja vain numeromuodossa")

            create_citation(tyyppi, author, publisher, year, title)
        if tyyppi == "article":
            author = request.form.get("author")
            journal = request.form.get("journal")
            year = request.form.get("year")
            title = request.form.get("title")
            if not author or not journal or not year or not title:
                raise ValueError("Täytä kaikki kentät")
            if len(author) > 500 or len(journal) > 500 or len(title) > 500:
                raise ValueError("Yhteen kenttään voi kirjoittaa max. 500 merkkiä")
            if int(year) > vuosi or year.isnumeric() is False:
                raise ValueError("Vuosiluvut 0-nykypäivä ovat sallittuja vain numeromuodossa")

            create_citation(tyyppi, author, None, year, title, journal)
        if tyyppi == "inproceedings":
            author = request.form.get("author")
            booktitle = request.form.get("booktitle")
            year = request.form.get("year")
            title = request.form.get("title")
            if not author or not booktitle or not year or not title:
                raise ValueError("Täytä kaikki kentät")
            if len(author) > 500 or len(booktitle) > 500 or len(title) > 500:
                raise ValueError("Yhteen kenttään voi kirjoittaa max. 500 merkkiä")
            if int(year) > vuosi or year.isnumeric() is False:
                raise ValueError("Vuosiluvut 0-nykypäivä ovat sallittuja vain numeromuodossa")
            create_citation(tyyppi, author, None, year, title, None, booktitle)

    except ValueError as error:
        flash(str(error))
        return redirect_to_sama_viite(tyyppi)

    return redirect("/")

@app.route("/bibtex")
def bibtex():
    cites = get_cites()
    return render_template("bibtex.html", cites=cites)

@app.route("/download_bibtex")
def download_bibtex():
    cites = get_cites()

    bibtex_cites = []

    for cite in cites:
        cite_type = cite[1]
        author = cite[2]
        title = cite[3]
        year = cite[4]
        publisher = cite[5] if len(cite) > 5 else None
        booktitle = cite[6] if len(cite) > 6 else None
        journal = cite[7] if len(cite) > 7 else None
        last_name = author.split()[-1]
        citation_key = f"{last_name}{year}"

        if cite_type == "article":
            bibtex_cites.append(f"""
@article{{{citation_key},
    author = "{author}",
    title = "{title}",
    journal = "{journal}",
    year = "{year}"
}}""")

        elif cite_type == "book":
            bibtex_cites.append(f"""
@book{{{citation_key},
    author = "{author}",
    title = "{title}",
    publisher = "{publisher}",
    year = "{year}"
}}""")

        elif cite_type == "inproceedings":
            bibtex_cites.append(f"""
@inproceedings{{{citation_key},
    author = "{author}",
    title = "{title}",
    booktitle = "{booktitle}",
    year = "{year}"
}}""")

    content = "\n\n".join(bibtex_cites)
    response = Response(
        content,
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment;filename=citations.bib"}
    )
    return response

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({'message': "db reset"})
