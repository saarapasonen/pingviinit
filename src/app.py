import datetime
from flask import redirect, render_template, request, jsonify, flash, url_for, Response, abort
from db_helper import reset_db, key_is_unique
from repositories.bibtex_repository import (
    get_cites, check_citation_type, get_cite_by_id,
    create_book_citation, create_article_citation, create_inproceedings_citation,
    remove_citation1, create_key, get_citation_id_by_key
)

from config import app, test_env
from util import convert_pages_to_first_and_last, check_existence

def redirect_to_uusi_viite():
    return redirect(url_for("render_uusi_viite"))

def redirect_to_sama_viite(tyyppi):
    return redirect(url_for("render_specific_type", tyyppi=tyyppi))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/uusi-viite")
def add_new():
    return render_template("uusi_viite.html")

@app.route("/lisatyt")
def lisatyt():
    cites = get_cites()
    return render_template("lisatyt.html", cites=cites)

@app.route("/muokkaa_viitetta/<int:viite_id>", methods=["GET"])
def edit_citation(viite_id):
    cite = get_cite_by_id(viite_id)
    firstpage, lastpage = convert_pages_to_first_and_last(cite.pages)
    return render_template("muokkaa_viitetta.html", cite=cite, firstpage=firstpage, \
                            lastpage=lastpage)

@app.route("/muokkaa_viitetta", methods=["POST"])
def edit_citation2():
    citation_id = int(request.form.get("id"))
    check_existence(citation_id)
    tyyppi = request.form.get("type")
    try:
        if tyyppi == "book":
            validate_book(citation_id)
            remove_citation1(citation_id)
            create_book_without_validation()
        if tyyppi == "article":
            validate_article(citation_id)
            remove_citation1(citation_id)
            create_article_without_validation()
        if tyyppi == "inproceedings":
            validate_inproceedings(citation_id)
            remove_citation1(citation_id)
            create_inproceedings_without_validation()

    except ValueError as error:
        flash(str(error))
        return redirect(f"/muokkaa_viitetta/{citation_id}")

    return redirect("/lisatyt")

def validate_book(citation_to_modify_id=None):
    vuosi = datetime.date.today().year
    author = request.form.get("author")
    publisher = request.form.get("publisher")
    year = request.form.get("year")
    title = request.form.get("title")
    key = request.form.get("key")
    if not author or not publisher or not year or not title:
        raise ValueError("Täytä kaikki kentät")
    if len(author) > 500 or len(publisher) > 500 or len(title) > 500:
        raise ValueError("Yhteen kenttään voi kirjoittaa max. 500 merkkiä")
    if int(year) > vuosi or year.isnumeric() is False:
        raise ValueError(
            "Vuosiluku tulee olla välillä 0-nyt. Vuosiluvun tulee olla numeromuodossa."
            )
    if not key_is_unique(key):
        if not citation_to_modify_id or get_citation_id_by_key(key) != citation_to_modify_id:
            raise ValueError(
                "Avaimen tulee olla uniikki! Vaihda toiseen tai jätä tyhjäksi, \
                      jolloin sivusto luo uniikin avaimen")

def validate_article(citation_to_modify_id=None):
    vuosi = datetime.date.today().year
    author = request.form.get("author")
    journal = request.form.get("journal")
    year = request.form.get("year")
    title = request.form.get("title")
    key = request.form.get("key")
    if not author or not journal or not year or not title:
        raise ValueError("Täytä kaikki kentät")
    if len(author) > 500 or len(journal) > 500 or len(title) > 500:
        raise ValueError("Yhteen kenttään voi kirjoittaa max. 500 merkkiä")
    if int(year) > vuosi or year.isnumeric() is False:
        raise ValueError(
            "Vuosiluku tulee olla välillä 0-nyt. Vuosiluvun tulee olla numeromuodossa."
            )
    if not key_is_unique(key):
        if not citation_to_modify_id or get_citation_id_by_key(key) != citation_to_modify_id:
            raise ValueError(
                "Avaimen tulee olla uniikki! Vaihda toiseen tai jätä tyhjäksi, \
                      jolloin sivusto luo uniikin avaimen")

def validate_inproceedings(citation_to_modify_id=None):
    vuosi = datetime.date.today().year
    author = request.form.get("author")
    booktitle = request.form.get("booktitle")
    year = request.form.get("year")
    title = request.form.get("title")
    key = request.form.get("key")
    if not author or not booktitle or not year or not title:
        raise ValueError("Täytä kaikki kentät")
    if len(author) > 500 or len(booktitle) > 500 or len(title) > 500:
        raise ValueError("Yhteen kenttään voi kirjoittaa max. 500 merkkiä")
    if int(year) > vuosi or year.isnumeric() is False:
        raise ValueError(
            "Vuosiluku tulee olla välillä 0-nyt. Vuosiluvun tulee olla numeromuodossa."
            )
    if not key_is_unique(key):
        if not citation_to_modify_id or get_citation_id_by_key(key) != citation_to_modify_id:
            raise ValueError(
                "Avaimen tulee olla uniikki! Vaihda toiseen tai jätä tyhjäksi, \
                      jolloin sivusto luo uniikin avaimen")

@app.route("/uusi_viite", methods=["GET"])
def render_uusi_viite():
    return render_template("uusi_viite.html")

@app.route("/luo-viite", methods=["POST"])
def select_citation_type():
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
    try:
        if tyyppi == "book":
            create_book()
        if tyyppi == "article":
            create_article()
        if tyyppi == "inproceedings":
            create_inproceedings()

    except ValueError as error:
        flash(str(error))
        return redirect_to_sama_viite(tyyppi)

    return redirect("/")

def create_book():
    vuosi = datetime.date.today().year
    author = request.form.get("author")
    publisher = request.form.get("publisher")
    year = request.form.get("year")
    title = request.form.get("title")
    if not author or not publisher or not year or not title:
        raise ValueError("Täytä kaikki kentät")
    if len(author) > 500 or len(publisher) > 500 or len(title) > 500:
        raise ValueError("Yhteen kenttään voi kirjoittaa max. 500 merkkiä")
    if int(year) > vuosi or year.isnumeric() is False:
        raise ValueError(
            "Vuosiluku tulee olla välillä 0-nyt. Vuosiluvun tulee olla numeromuodossa."
            )
    key = request.form.get("key")
    if not key_is_unique(key):
        raise ValueError(
            "Avaimen tulee olla uniikki! Vaihda toiseen tai jätä tyhjäksi, \
                  jolloin sivusto luo uniikin avaimen")
    if key == "":
        key = create_key(author, year)

    volume = request.form.get("volume")
    number = request.form.get("number")
    series = request.form.get("series")
    address = request.form.get("address")
    edition = request.form.get("edition")
    month = request.form.get("month")
    note = request.form.get("note")
    tyyppi = request.form.get("type")

    create_book_citation(tyyppi, key, author, publisher, year, title, volume, number,
                         series, address, edition, month, note)

def create_article():
    vuosi = datetime.date.today().year
    author = request.form.get("author")
    journal = request.form.get("journal")
    year = request.form.get("year")
    title = request.form.get("title")
    if not author or not journal or not year or not title:
        raise ValueError("Täytä kaikki kentät")
    if len(author) > 500 or len(journal) > 500 or len(title) > 500:
        raise ValueError("Yhteen kenttään voi kirjoittaa max. 500 merkkiä")
    if int(year) > vuosi or year.isnumeric() is False:
        raise ValueError(
            "Vuosiluku tulee olla välillä 0-nyt. Vuosiluvun tulee olla numeromuodossa."
            )

    key = request.form.get("key")
    if not key_is_unique(key):
        raise ValueError(
            "Avaimen tulee olla uniikki! Vaihda toiseen tai jätä tyhjäksi, \
                  jolloin sivusto luo uniikin avaimen")
    if key == "":
        key = create_key(author, year)

    volume = request.form.get("volume")
    number = request.form.get("number")
    firstpage = request.form.get("firstpage")
    lastpage = request.form.get("lastpage")
    pages = f"{firstpage}--{lastpage}"
    month = request.form.get("month")
    doi = request.form.get("doi")
    note = request.form.get("note")
    tyyppi = request.form.get("type")

    create_article_citation(tyyppi, key, author, journal, year, title, volume, number, pages,
                            month, doi, note)

def create_inproceedings():
    vuosi = datetime.date.today().year
    author = request.form.get("author")
    booktitle = request.form.get("booktitle")
    year = request.form.get("year")
    title = request.form.get("title")
    if not author or not booktitle or not year or not title:
        raise ValueError("Täytä kaikki kentät")
    if len(author) > 500 or len(booktitle) > 500 or len(title) > 500:
        raise ValueError("Yhteen kenttään voi kirjoittaa max. 500 merkkiä")
    if int(year) > vuosi or year.isnumeric() is False:
        raise ValueError(
            "Vuosiluku tulee olla välillä 0-nyt. Vuosiluvun tulee olla numeromuodossa."
            )
    key = request.form.get("key")
    if not key_is_unique(key):
        raise ValueError(
            "Avaimen tulee olla uniikki! Vaihda toiseen tai jätä tyhjäksi, \
                  jolloin sivusto luo uniikin avaimen")
    if key == "":
        key = create_key(author, year)

    editor = request.form.get("editor")
    volume = request.form.get("volume")
    number = request.form.get("number")
    series = request.form.get("series")
    firstpage = request.form.get("firstpage")
    lastpage = request.form.get("lastpage")
    pages = f"{firstpage}--{lastpage}"
    address = request.form.get("address")
    month = request.form.get("month")
    organization = request.form.get("organization")
    publisher = request.form.get("publisher")
    note = request.form.get("note")
    tyyppi = request.form.get("type")

    create_inproceedings_citation(tyyppi, key, author, year, title, booktitle, editor,
                                  volume, number, series, pages, address, month, organization,
                                  publisher, note)

def create_book_without_validation():
    author = request.form.get("author")
    publisher = request.form.get("publisher")
    year = request.form.get("year")
    title = request.form.get("title")
    key = request.form.get("key")
    if key == "":
        key = create_key(author, year)
    volume = request.form.get("volume")
    number = request.form.get("number")
    series = request.form.get("series")
    address = request.form.get("address")
    edition = request.form.get("edition")
    month = request.form.get("month")
    note = request.form.get("note")
    tyyppi = request.form.get("type")

    create_book_citation(tyyppi, key, author, publisher, year, title, volume, number,
                         series, address, edition, month, note)

def create_article_without_validation():
    author = request.form.get("author")
    journal = request.form.get("journal")
    year = request.form.get("year")
    title = request.form.get("title")
    key = request.form.get("key")
    if key == "":
        key = create_key(author, year)
    volume = request.form.get("volume")
    number = request.form.get("number")
    firstpage = request.form.get("firstpage")
    lastpage = request.form.get("lastpage")
    pages = f"{firstpage}--{lastpage}"
    month = request.form.get("month")
    doi = request.form.get("doi")
    note = request.form.get("note")
    tyyppi = request.form.get("type")

    create_article_citation(tyyppi, key, author, journal, year, title, volume, number, pages,
                            month, doi, note)

def create_inproceedings_without_validation():
    author = request.form.get("author")
    booktitle = request.form.get("booktitle")
    year = request.form.get("year")
    title = request.form.get("title")
    key = request.form.get("key")
    if key == "":
        key = create_key(author, year)
    editor = request.form.get("editor")
    volume = request.form.get("volume")
    number = request.form.get("number")
    series = request.form.get("series")
    firstpage = request.form.get("firstpage")
    lastpage = request.form.get("lastpage")
    pages = f"{firstpage}--{lastpage}"
    address = request.form.get("address")
    month = request.form.get("month")
    organization = request.form.get("organization")
    publisher = request.form.get("publisher")
    note = request.form.get("note")
    tyyppi = request.form.get("type")

    create_inproceedings_citation(tyyppi, key, author, year, title, booktitle, editor,
                                  volume, number, series, pages, address, month, organization,
                                  publisher, note)

@app.route("/bibtex")
def bibtex():
    cites = get_cites()
    return render_template("bibtex.html", cites=cites)

def create_bibtex(cite_type, key, author, title, **kwargs):
    fields = [
        f"    author = \"{author}\"",
        f"    title = \"{title}\"",
    ]

    for field, value in kwargs.items():
        if value is not None and value != "":
            fields.append(f"    {field} = \"{value}\"")

    fields_str = ",\n".join(fields)
    return f"@{cite_type}{{{key},\n{fields_str}\n}}"

@app.route("/download_bibtex")
def download_bibtex():
    cites = get_cites()

    bibtex_cites = []

    for cite in cites:
        cite_fields = {
            'cite_type': cite[1],
            'key': cite[2],
            'author': cite[3],
            'title': cite[4],
            'year': cite[5] if len(cite) > 5 else None,
            'publisher': cite[6] if len(cite) > 6 else None,
            'booktitle': cite[7] if len(cite) > 7 else None,
            'journal': cite[8] if len(cite) > 8 else None,
            'volume': cite[9] if len(cite) > 9 else None,
            'number': cite[10] if len(cite) > 10 else None,
            'series': cite[11] if len(cite) > 11 else None,
            'address': cite[12] if len(cite) > 12 else None,
            'edition': cite[13] if len(cite) > 13 else None,
            'month': cite[14] if len(cite) > 14 else None,
            'editor': cite[15] if len(cite) > 15 else None,
            'pages': cite[16] if len(cite) > 16 else None,
            'organization': cite[17] if len(cite) > 17 else None,
            'doi': cite[18] if len(cite) > 18 else None,
            'note': cite[19] if len(cite) > 19 else None
        }

        if cite_fields['cite_type'] == "article":
            bibtex_entry = create_bibtex(
                "article", cite_fields['key'], cite_fields['author'],
                cite_fields['title'],journal=cite_fields['journal'],
                year=cite_fields['year'],
                volume=cite_fields['volume'],
                number=cite_fields['number'],
                pages=cite_fields['pages'],
                month=cite_fields['month'], doi=cite_fields['doi'],
                note=cite_fields['note']
            )
            bibtex_cites.append(bibtex_entry)

        elif cite_fields['cite_type'] == "book":
            bibtex_entry = create_bibtex(
                "book", cite_fields['key'], cite_fields['author'],
                cite_fields['title'], publisher=cite_fields['publisher'],
                year=cite_fields['year'],
                volume=cite_fields['volume'],
                number=cite_fields['number'],
                series=cite_fields['series'],
                address=cite_fields['address'], edition=cite_fields['edition'],
                month=cite_fields['month'], note=cite_fields['note']
            )
            bibtex_cites.append(bibtex_entry)

        elif cite_fields['cite_type'] == "inproceedings":
            bibtex_entry = create_bibtex(
                "inproceedings", cite_fields['key'], cite_fields['author'],
                cite_fields['title'], booktitle=cite_fields['booktitle'],
                year=cite_fields['year'],
                editor=cite_fields['editor'],
                volume=cite_fields['volume'],
                number=cite_fields['number'],
                series=cite_fields['series'], pages=cite_fields['pages'],
                address=cite_fields['address'], month=cite_fields['month'],
                organization=cite_fields['organization'], publisher=cite_fields['publisher'],
                note=cite_fields['note']
            )
            bibtex_cites.append(bibtex_entry)

    content = "\n\n".join(bibtex_cites)
    response = Response(
        content,
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment;filename=citations.bib"}
    )
    return response

@app.route("/poista-viite", methods=["POST"])
def remove_citation():
    id1 = int(request.form.get("id"))
    if id1 not in [int(citation.id) for citation in get_cites()]:
        abort(403)
    remove_citation1(id1)
    return redirect("/lisatyt")

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({'message': "db reset"})
