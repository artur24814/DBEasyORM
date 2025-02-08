import psycopg2
from .abstract import DataBaseBackend
from dbeasyorm.fields import BaseField, ForeignKey
from dbeasyorm.db.operators import apply_sql_operator


class PostgreSQLBackend(DataBaseBackend):
    def __init__(self, host, database: str, user: str, password: str, port=5432, *args, **kwargs):
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

    def get_foreign_key_constraint(self, field_name: str, related_table: str, on_delete: str) -> str:
        return (
            f"{field_name} INTEGER, "
            f"CONSTRAINT fk_{field_name}_to_{related_table} "
            f"FOREIGN KEY ({field_name}) REFERENCES {related_table} (_id) "
            f"ON DELETE {on_delete}"
        )

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
            where_sql = " WHERE " + " AND ".join([apply_sql_operator(col, val) for col, val in where_clause.items()])

        limit_offset_sql = ""
        if limit is not None:
            limit_offset_sql = f" LIMIT {limit}"
        if offset is not None:
            limit_offset_sql += f" OFFSET {offset}"

        return f"SELECT {', '.join(columns) if columns else '*'} FROM {table_name}{where_sql}{limit_offset_sql}"

    def generate_join_sql(self, table_name: str, on: str, join_type: str) -> str:
        return f" {join_type} JOIN {table_name} ON {on}"

    def generate_update_sql(self, table_name: str, set_clause: tuple, where_clause: tuple):
        set_sql = ', '.join([f"{col} = {self.get_placeholder()}" for col in set_clause])
        where_sql = " AND ".join([f"{col} = {self.get_placeholder()}" for col in where_clause]) if where_clause else ""
        return f"UPDATE {table_name} SET {set_sql} WHERE {where_sql} RETURNING *"

    def generate_delete_sql(self, table_name: str, where_clause: tuple):
        where_sql = " AND ".join([f"{col} = {self.get_placeholder()}" for col in where_clause]) if where_clause else ""
        return f"DELETE FROM {table_name} WHERE {where_sql} RETURNING *"

    def generate_create_table_sql(self, table_name: str, fields: BaseField):
        columns = []
        foreign_keys = []

        for field in fields:
            if isinstance(field, ForeignKey):
                foreign_keys.append(
                    field.get_sql_line(self.get_foreign_key_constraint)
                )
            else:
                columns.append(
                    field.get_sql_line(sql_type=self.get_sql_type(field.python_type))
                )
        table_body = ", \n".join(columns + foreign_keys)
        return f"""CREATE TABLE IF NOT EXISTS {table_name} ({table_body});"""

    def generate_alter_field_sql(self, table_name: str, field: BaseField, *args, **kwargs) -> str:
        if isinstance(field, ForeignKey):
            field_sql = field.get_sql_line(self.get_foreign_key_constraint)
        else:
            field_sql = field.get_sql_line(sql_type=self.get_sql_type(field.python_type))
        return f"ALTER TABLE {table_name} ADD {field_sql};"

    def generate_drop_field_sql(self, table_name: str, field: BaseField, *args, **kwargs) -> str:
        return f"ALTER TABLE {table_name} DROP COLUMN {field};"

    def generate_drop_table_sql(self, table_name: str) -> str:
        return f"DROP TABLE {table_name}"

    def get_database_schemas(self) -> dict:
        schema = {}

        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()
        for table in tables:
            table_name = table[0]
            if table_name == 'sqlite_sequence':
                continue

            self.cursor.execute(f"PRAGMA table_info({table_name});")
            columns = self.cursor.fetchall()
            schema[table_name] = {col[1]: col[2] for col in columns}

        return schema
