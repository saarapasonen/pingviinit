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

def set_done(todo_id):
    sql = text("UPDATE todos SET done = TRUE WHERE id = :id")
    db.session.execute(sql, { "id": todo_id })
    db.session.commit()

def create_citation(type, author=None, publisher=None, year=None, title=None, journal=None, booktitle=None):
    sql = text("INSERT INTO citations (type, author, publisher, year, title, journal, booktitle) VALUES (:type, :author, :publisher, :year, :title, :journal, :booktitle)")
    db.session.execute(sql, {"type": type, "author": author, "publisher": publisher, "year": year, "title": title, "journal": journal, "booktitle": booktitle})
    db.session.commit()
