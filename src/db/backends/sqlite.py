import sqlite3
from .abstract import DataBaseBackend
from src.fields import BaseField, ForeignKey


class SQLiteBackend(DataBaseBackend):
    def __init__(self, database_path: str):
        self.database_path = database_path
        self.cursor = None
        self.connection = None
        self.type_map = self.get_sql_types_map()

    def get_placeholder(self) -> str:
        return "?"

    def get_sql_type(self, type) -> str:
        return self.type_map.get(type)

    def get_sql_types_map(self) -> dict:
        return {
            int: "INTEGER",
            float: "REAL",
            bytes: "BLOB",
            bool: "INTEGER",
            str: "TEXT"
        }

    def get_foreign_key_constraint(self, field_name: str, related_table: str, on_delete: str) -> str:
        return (
            f"FOREIGN KEY ({field_name}) REFERENCES {related_table} (id) "
            f"ON DELETE {on_delete}"
        )

    def connect(self, **kwargs) -> DataBaseBackend:
        self.connection = sqlite3.connect(self.database_path)
        self.cursor = self.connection.cursor()
        return self

    def execute(self, query: str, params=None) -> sqlite3.Cursor:
        self.cursor.execute(query, params or ())
        self.connection.commit()
        return self.cursor

    def generate_insert_sql(self, table_name: str, columns: tuple) -> str:
        columns_str = ', '.join(columns)
        placeholders = ', '.join([self.get_placeholder() for _ in columns])
        return f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"

    def generate_select_sql(self, table_name: str, columns: tuple, where_clause: dict = None, limit: int = None, offset: int = None) -> str:
        where_sql = ""
        if where_clause:
            where_sql = " WHERE " + " AND ".join([f"{col} = " + self.get_sql_val_repr(val) for col, val in where_clause.items()])

        limit_offset_sql = ""
        if limit is not None:
            limit_offset_sql = f" LIMIT {limit}"
        if offset is not None:
            limit_offset_sql += f" OFFSET {offset}"

        return f"SELECT {', '.join(columns) if columns else '*'} FROM {table_name}{where_sql}{limit_offset_sql}"

    def generate_update_sql(self, table_name: str, set_clause: tuple, where_clause: tuple):
        set_sql = ', '.join([f"{col}={self.get_placeholder()}" for col in set_clause])
        where_sql = " AND ".join([f"{col}={self.get_placeholder()}" for col in where_clause]) if where_clause else ""
        return f"UPDATE {table_name} SET {set_sql} WHERE {where_sql}"

    def generate_delete_sql(self, table_name: str, where_clause: tuple):
        where_sql = " AND ".join([f"{col}={self.get_placeholder()}" for col in where_clause]) if where_clause else ""
        return f"DELETE FROM {table_name} WHERE {where_sql}"

    def generate_migrate_table(self, table_name: str, fields: BaseField):
        table_body = ", \n".join([
            field.get_sql_line(self.get_foreign_key_constraint)
            if isinstance(field, ForeignKey)
            else field.get_sql_line(sql_type=self.get_sql_type(field.python_type))
            for field in fields
        ])
        return f"""CREATE TABLE IF NOT EXISTS {table_name} ({table_body});"""
