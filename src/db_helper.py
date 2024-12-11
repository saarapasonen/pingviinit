from sqlalchemy import text
from config import db, app

TABLE_NAME = "citations"


def table_exists(name):
    sql_table_existence = text(
        "SELECT EXISTS ("
        "  SELECT 1"
        "  FROM information_schema.tables"
        f" WHERE table_name = '{name}'"
        ")"
    )

    print(f"Checking if table {name} exists")
    print(sql_table_existence)

    result = db.session.execute(sql_table_existence)
    return result.fetchall()[0][0]

def key_is_unique(key):
    sql_check_key = text(f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE key = :key")
    result = db.session.execute(sql_check_key, {"key": key})
    return result.fetchone()[0] == 0

def reset_db():
    print(f"Clearing contents from table {TABLE_NAME}")
    sql = text(f"DELETE FROM {TABLE_NAME}")
    db.session.execute(sql)
    db.session.commit()


def setup_db():
    if table_exists(TABLE_NAME):
        print(f"Table {TABLE_NAME} exists, dropping")
        sql = text(f"DROP TABLE {TABLE_NAME}")
        db.session.execute(sql)
        db.session.commit()

    print(f"Creating table {TABLE_NAME}")
    sql = text(
        f"CREATE TABLE {TABLE_NAME} ("
        "  id SERIAL PRIMARY KEY, "
        "  type TEXT,"
        "  key TEXT UNIQUE,"
        "  author TEXT,"
        "  title TEXT,"
        "  year TEXT,"
        "  publisher TEXT,"
        "  booktitle TEXT,"
        "  journal TEXT,"
        "  volume TEXT,"
        "  number TEXT,"
        "  series TEXT,"
        "  address TEXT,"
        "  edition TEXT,"
        "  month TEXT,"
        "  editor TEXT,"
        "  pages TEXT,"
        "  organization TEXT,"
        "  doi TEXT,"
        "  note TEXT"
        ")"
    )

    db.session.execute(sql)
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        setup_db()
