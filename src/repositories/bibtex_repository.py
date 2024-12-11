from random import randint
from sqlalchemy import text
from config import db
from db_helper import key_is_unique

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

def create_book_citation(tyyppi, key=None, author=None, publisher=None, year=None, title=None,
                         volume=None, number=None, series=None, address=None, edition=None,
                         month=None, note=None):
    sql = text("INSERT INTO citations (type, key, author, publisher, year, title, \
               volume, number, series, address, edition, month, note) \
        VALUES (:type, :key, :author, :publisher, :year, :title, \
               :volume, :number, :series, :address, :edition, :month, :note)")
    db.session.execute(sql, {"type": tyyppi, "key": key, "author": author, "publisher": publisher,
                             "year": year, "title": title, "volume":volume, "number": number,
                             "series":series, "address":address, "edition":edition, "month":month,
                             "note":note})
    db.session.commit()

def create_article_citation(tyyppi, key=None, author=None, journal=None, year=None, title=None,
                            volume=None, number=None, pages=None, month=None, doi=None, note=None):
    sql = text("INSERT INTO citations (type, key, author, year, title, journal, \
                volume, number, month, pages, doi, note) \
        VALUES (:type, :key, :author, :year, :title, :journal, :volume, :number, :month, :pages, \
               :doi, :note)")
    db.session.execute(sql, {"type": tyyppi, "key": key, "author": author, "year": year,
                             "title": title, "journal": journal, "volume":volume, "number":number,
                             "month":month, "pages":pages, "doi":doi, "note":note})
    db.session.commit()

def create_inproceedings_citation(tyyppi, key=None, author=None, year=None, title=None,
                                  booktitle=None, editor=None, volume=None, number=None,
                                  series=None, pages=None, address=None, month=None,
                                  organization=None, publisher=None, note=None):
    sql = text("INSERT INTO citations (type, key, author, publisher, year, title, booktitle, \
               volume, number, series, address, month, editor, pages, organization, note) \
        VALUES (:type, :key, :author, :publisher, :year, :title, :booktitle, \
               :volume, :number, :series, :address, :month, :editor, :pages, \
               :organization, :note)")
    db.session.execute(sql, {"type": tyyppi, "key": key, "author": author, "publisher": publisher,
                             "year": year, "title": title, "booktitle": booktitle,
                             "volume":volume, "number":number, "series":series, "address":address,
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


def create_key(author, year):
    last_name = author.split()[-1]
    key = last_name + year + str(randint(0, 1000))
    while not key_is_unique(key):
        key = key + str(randint(0, 1000))

    return key
