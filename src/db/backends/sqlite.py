import sqlite3
from .abstract import DataBaseBackend


class SQLiteBackend(DataBaseBackend):
    def __init__(self, database_path):
        self.database_path = database_path
        self.connection = None

    def connect(self, **kwargs):
        self.connection = sqlite3.connect(self.database_path)
        self.cursor = self.connection.cursor()

    def execute(self, query, params=None):
        self.cursor.execute(query, params or ())
        self.connection.commit()
        return self.cursor.fetchall()
