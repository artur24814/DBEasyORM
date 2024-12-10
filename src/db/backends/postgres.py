import psycopg2
from .abstract import DataBaseBackend


class PostgreSQLBackend(DataBaseBackend):
    def __init__(self, host, database: str, user: str, password: str, port=5432):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.cursor = None
        self.connection = None
        self.type_map = self.get_sql_types_map()

    def get_placeholder(self) -> str:
        return "%s"

    def get_sql_type(self, type) -> str:
        return self.type_map.get(type)

    def get_sql_types_map(self) -> dict:
        return {
            int: "INTEGER",
            float: "DOUBLE PRECISION",
            bytes: "BYTEA",
            bool: "BOOLEAN",
            str: "VARCHAR"
        }

    def connect(self, **kwargs) -> DataBaseBackend:
        self.connection = psycopg2.connect(
            host=self.host, database=self.database, user=self.user, password=self.password, port=self.port
        )
        self.cursor = self.connection.cursor()
        return self

    def execute(self, query: str, params=None) -> psycopg2.extensions.cursor:
        self.cursor.execute(query, params or ())
        self.connection.commit()
        return self.cursor

    def generate_insert_sql(self, table_name: str, columns: tuple) -> str:
        columns_str = ', '.join(columns)
        placeholders = ', '.join([self.get_placeholder() for _ in columns])
        return f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders}) RETURNING id"

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
        set_sql = ', '.join([f"{col} = {self.get_placeholder()}" for col in set_clause])
        where_sql = " AND ".join([f"{col} = {self.get_placeholder()}" for col in where_clause]) if where_clause else ""
        return f"UPDATE {table_name} SET {set_sql} WHERE {where_sql} RETURNING *"

    def generate_delete_sql(self, table_name: str, where_clause: tuple):
        where_sql = " AND ".join([f"{col} = {self.get_placeholder()}" for col in where_clause]) if where_clause else ""
        return f"DELETE FROM {table_name} WHERE {where_sql} RETURNING *"
