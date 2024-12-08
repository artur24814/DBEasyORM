import sqlite3
from .abstract import DataBaseBackend


class SQLiteBackend(DataBaseBackend):
    def __init__(self, database_path: str):
        self.database_path = database_path
        self.cursor = None
        self.connection = None
        self.type_map = self.get_sql_types_map()

    def get_placeholder(self) -> str:
        return "?"

    def get_sql_type(self, type):
        return self.type_map.get(type)

    def get_sql_types_map(self) -> dict:
        return {
            int: "INTEGER",
            float: "REAL",
            bytes: "BLOB",
            bool: "INTEGER",
            str: "TEXT"
        }

    def connect(self, **kwargs) -> DataBaseBackend:
        self.connection = sqlite3.connect(self.database_path)
        self.cursor = self.connection.cursor()
        return self

    def execute(self, query: str, params=None) -> sqlite3.Cursor:
        self.cursor.execute(query, params or ())
        self.connection.commit()
        return self.cursor

    def generate_insert_sql(self, table_name: str, columns: tuple, placeholders: tuple) -> str:
        return f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    def generate_select_sql(self, table_name: str, columns: tuple, where_clause: tuple, limit: int = None, offset: int = None) -> str:
        where_sql = ""
        if where_clause:
            where_sql = " WHERE " + " AND ".join([f"{col} = {val}" for col, val in zip(where_clause[0], where_clause[1])])

        limit_offset_sql = ""
        if limit is not None:
            limit_offset_sql = f" LIMIT {limit}"
        if offset is not None:
            limit_offset_sql += f" OFFSET {offset}"

        return f"SELECT {', '.join(columns)} FROM {table_name}{where_sql}{limit_offset_sql}"

    def generate_update_sql(self, table_name, set_clause, where_clause):
        return f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"

    def generate_delete_sql(self, table_name, where_clause):
        return f"DELETE FROM {table_name} WHERE {where_clause}"
