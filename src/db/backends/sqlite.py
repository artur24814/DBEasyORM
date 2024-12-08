import sqlite3
from .abstract import DataBaseBackend


class SQLiteBackend(DataBaseBackend):
    def __init__(self, database_path: str):
        self.database_path = database_path
        self.cursor = None
        self.connection = None

    def connect(self, **kwargs) -> DataBaseBackend:
        self.connection = sqlite3.connect(self.database_path)
        self.cursor = self.connection.cursor()
        return self

    def execute(self, query: str, params=None) -> sqlite3.Cursor:
        self.cursor.execute(query, params or ())
        self.connection.commit()
        return self.cursor
