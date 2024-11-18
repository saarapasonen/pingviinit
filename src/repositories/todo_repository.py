from config import db
from sqlalchemy import text

from entities.todo import Todo

def get_cites():
    result = db.session.execute(text("SELECT * FROM citations"))
    cites = result.fetchall()
    return cites

def set_done(todo_id):
    sql = text("UPDATE todos SET done = TRUE WHERE id = :id")
    db.session.execute(sql, { "id": todo_id })
    db.session.commit()

def create_citation(type, author=None, publisher=None, year=None, title=None, journal=None, booktitle=None):
    sql = text("INSERT INTO citations (author, publisher, year, title, journal, booktitle) VALUES (:author, :publisher, :year, :title, :journal, :booktitle)")
    db.session.execute(sql, { "author": author, "publisher": publisher, "year": year, "title": title, "journal": journal, "booktitle": booktitle})
    db.session.commit()
