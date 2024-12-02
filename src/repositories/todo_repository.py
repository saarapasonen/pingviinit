from sqlalchemy import text
from config import db


def check_citation_type(content):
    if content == "valitseviite":
        raise ValueError("Valitse viitetyyppi")

    return content


def get_cites():
    result = db.session.execute(text("SELECT * FROM citations"))
    cites = result.fetchall()
    return cites

def get_cite_by_id(viite_id):
    sql = text("SELECT * FROM citations WHERE id = :id")
    result = db.session.execute(sql, {"id": viite_id})
    return result.fetchone()


def set_done(todo_id):
    sql = text("UPDATE cites SET done = TRUE WHERE id = :id")
    db.session.execute(sql, {"id": todo_id})
    db.session.commit()


def create_citation(tyyppi, key=None, author=None, publisher=None, year=None,
                    title=None, journal=None, booktitle=None, volumenumber=None,
                    series=None, address=None, edition=None, month=None, editor=None,
                    pages=None, organization=None, doi=None, note=None):
    sql = text("INSERT INTO citations (type, key, author, publisher, year, title, journal, \
               booktitle, volumenumber, series, address, edition, month, editor, pages, \
               organization, doi, note) \
        VALUES (:type, :key, :author, :publisher, :year, :title, :journal, :booktitle, \
               :volumenumber, :series, :address, :edition, :month, :editor, :pages, \
               :organization, :doi, :note)")
    db.session.execute(sql, {"type": tyyppi, "key": key, "author": author, "publisher": publisher,
                             "year": year, "title": title, "journal": journal,
                             "booktitle": booktitle, "volumenumber":volumenumber, "series":series,
                             "address":address, "edition":edition, "month":month, "editor":editor,
                             "pages":pages, "organization":organization, "doi":doi, "note":note})
    db.session.commit()

def create_book_citation(tyyppi, key=None, author=None, publisher=None, year=None, title=None,
                         volumenumber=None, series=None, address=None, edition=None, month=None,
                         note=None):
    sql = text("INSERT INTO citations (type, key, author, publisher, year, title, \
               volumenumber, series, address, edition, month, note) \
        VALUES (:type, :key, :author, :publisher, :year, :title, \
               :volumenumber, :series, :address, :edition, :month, :note)")
    db.session.execute(sql, {"type": tyyppi, "key": key, "author": author, "publisher": publisher,
                             "year": year, "title": title, "volumenumber":volumenumber,
                             "series":series, "address":address, "edition":edition, "month":month,
                             "note":note})
    db.session.commit()

def create_article_citation(tyyppi, key=None, author=None, journal=None, year=None, title=None,
                            volumenumber=None, pages=None, month=None, doi=None, note=None):
    sql = text("INSERT INTO citations (type, key, author, year, title, journal, \
                volumenumber, month, pages, doi, note) \
        VALUES (:type, :key, :author, :year, :title, :journal, :volumenumber, :month, :pages, \
               :doi, :note)")
    db.session.execute(sql, {"type": tyyppi, "key": key, "author": author, "year": year,
                             "title": title, "journal": journal, "volumenumber":volumenumber,
                             "month":month, "pages":pages, "doi":doi, "note":note})
    db.session.commit()

def create_inproceedings_citation(tyyppi, key=None, author=None, year=None, title=None,
                                  booktitle=None, editor=None, volumenumber=None, series=None,
                                  pages=None, address=None, month=None, organization=None,
                                  publisher=None, note=None):
    sql = text("INSERT INTO citations (type, key, author, publisher, year, title, booktitle, \
               volumenumber, series, address, month, editor, pages, organization, note) \
        VALUES (:type, :key, :author, :publisher, :year, :title, :booktitle, \
               :volumenumber, :series, :address, :month, :editor, :pages, \
               :organization, :note)")
    db.session.execute(sql, {"type": tyyppi, "key": key, "author": author, "publisher": publisher,
                             "year": year, "title": title, "booktitle": booktitle,
                             "volumenumber":volumenumber, "series":series, "address":address,
                             "month":month, "editor":editor, "pages":pages,
                             "organization":organization, "note":note})
    db.session.commit()

def update_citation(viite_id, values):
    sql = text("""
        UPDATE citations
        SET type = :type, author = :author, publisher = :publisher,
            year = :year, title = :title, journal = :journal, booktitle = :booktitle
        WHERE id = :id
    """)
    keys = ["type", "author", "publisher", "year", "title", "journal", "booktitle"]
    data = dict(zip(keys, values))
    data['id'] = viite_id
    db.session.execute(sql, data)
    db.session.commit()

def remove_citation1(id1):
    sql = "DELETE FROM citations WHERE id=:id"
    db.session.execute(text(sql), {"id":id1})
    db.session.commit()
