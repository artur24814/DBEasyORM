import sqlite3


def test_connection(sqlite_backend):
    assert sqlite_backend.cursor is None
    assert sqlite_backend.connection is None
    sqlite_backend.connect()

    assert sqlite_backend.cursor is not None
    assert sqlite_backend.connection is not None

    assert isinstance(sqlite_backend.cursor, sqlite3.Cursor) is True
    assert isinstance(sqlite_backend.connection, sqlite3.Connection) is True


def test_exeqution_query(sqlite_backend):
    query_create_table = """
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        age INTEGER
    );
    """
    query_insert_into_tabe = "INSERT INTO Users (name, email, age)  VALUES (?, ?, ?);"
    sqlite_backend.connect()

    sqlite_backend.execute(query=query_create_table)
    sqlite_backend.execute(query=query_insert_into_tabe, params=('Jan Kowalski', 'jan.kowalski@example.com', 30))
