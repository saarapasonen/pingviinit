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


def create_citation(type1, author=None, publisher=None, year=None,
                    title=None, journal=None, booktitle=None):
    sql = text("INSERT INTO citations (type, author, publisher, year, title, journal, booktitle) \
        VALUES (:type, :author, :publisher, :year, :title, :journal, :booktitle)")
    db.session.execute(sql, {"type": type1, "author": author, "publisher": publisher, "year": year,
                             "title": title, "journal": journal, "booktitle": booktitle})
    db.session.commit()


def update_citation(viite_id, type1, author, publisher, year,
                    title, journal=None, booktitle=None):
    sql = text("""
        UPDATE citations
        SET type = :type, author = :author, publisher = :publisher,
            year = :year, title = :title, journal = :journal, booktitle = :booktitle
        WHERE id = :id
    """)
    db.session.execute(sql, {"type": type1, "author": author, "publisher": publisher,
                            "year": year, "title": title,
                            "journal": journal, "booktitle": booktitle,
                            "id": viite_id})
    db.session.commit()
