from config import db
from sqlalchemy import text

from entities.todo import Todo

def get_todos():
    result = db.session.execute(text("SELECT id, content, done FROM todos"))
    todos = result.fetchall()
    return [Todo(todo[0], todo[1], todo[2]) for todo in todos] 

def set_done(todo_id):
    sql = text("UPDATE todos SET done = TRUE WHERE id = :id")
    db.session.execute(sql, { "id": todo_id })
    db.session.commit()

def create_citation(type, author=None, publisher=None, year=None, title=None, journal=None, booktitle=None):
    sql = text("INSERT INTO citations (author, publisher, year, title, journal, booktitle) VALUES (:author, :publisher, :year, :title, :journal, :booktitle)")
    db.session.execute(sql, { "author": author, "publisher": publisher, "year": year, "title": title, "journal": journal, "booktitle": booktitle})
    db.session.commit()
